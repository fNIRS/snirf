from __future__ import annotations

import h5py
import numpy as np
import os
import re

from pydantic import (BaseModel, ConfigDict, AfterValidator, ValidationError,
                      ValidationInfo, model_validator, field_validator)
from pydantic_core import PydanticCustomError
from typing import Optional, Annotated, Any

os.environ['PYDANTIC_ERRORS_INCLUDE_URL'] = 'false'
GREEN = '\033[32m'
ORANGE = '\033[33m'
RED = '\033[31m'
RESET = '\033[0m'

RECOGNIZED_INDEXED_PREFIXES = [
    'nirs',
    'data',
    'stim',
    'aux',
    'measurementList'
]
RECOGNIZED_COORDINATE_SYSTEMS = [
    'ICBM452AirSpace',
    'ICBM452Warp5Space',
    'IXI549Space',
    'fsaverage',
    'fsaverageSym',
    'fsLR',
    'MNIColin27',
    'MNI152Lin',
    'MNI152NLin2009[a-c][Sym|Asym]',
    'MNI152NLin6Sym',
    'MNI152NLin6ASym',
    'MNI305',
    'NIHPD',
    'OASIS30AntsOASISAnts',
    'OASIS30Atropos',
    'Talairach',
    'UNCInfant',
]
RECOGNIZED_DATA_TYPES = [
    1,
    51,
    101,
    102,
    151,
    152,
    201,
    251,
    301,
    351,
    401,
    410,
    99999,
]
RECOGNIZED_DATA_TYPE_LABELS = [
    'dOD',
    'dMean',
    'dVar',
    'dSkew',
    'mua',
    'musp',
    'HbO',
    'HbR',
    'HbT',
    'H2O',
    'Lipid',
    'StO2',
    'BFi',
    'HRF dOD',
    'HRF dMean',
    'HRF dVar',
    'HRF dSkew',
    'HRF HbO',
    'HRF HbR',
    'HRF HbT',
    'HRF BFi',
]


# ======================================================================================
# TYPE HELPERS
# ======================================================================================
def check_nnint(v: np.integer) -> np.integer:
    if not v >= 0:
        raise PydanticCustomError(
            "nnint_type",
            "Input should be a valid integer greater than or equal to 0"
        )
    return v


def check_nnint_1d(v: np.ndarray) -> np.ndarray:
    if not (
        v.ndim == 1
        and np.issubdtype(v.dtype, np.integer)
        and np.all(v >= 0)
    ):
        raise PydanticCustomError(
            "nnint_1d_ndarray",
            "Input should be a valid 1D array of integers greater than or equal to 0"
        )
    return v


def check_float_1d(v: np.ndarray) -> np.ndarray:
    if not (
        v.ndim == 1
        and np.issubdtype(v.dtype, np.floating)
    ):
        raise PydanticCustomError(
            "float_1d_ndarray",
            "Input should be a valid 1D array of floats"
        )
    return v


def check_float_2d(v: np.ndarray) -> np.ndarray:
    if not (
        v.ndim == 2
        and np.issubdtype(v.dtype, np.floating)
    ):
        raise PydanticCustomError(
            "float_2d_ndarray",
            "Input should be a valid 2D array of floats"
        )
    return v


def check_string_1d(v: np.ndarray) -> np.ndarray:
    if not (
        v.ndim == 1
        and v.dtype == object
        and all(isinstance(x, (str, bytes)) for x in v.flat)
    ):
        raise PydanticCustomError(
            "string_1d_ndarray",
            "Input should be a valid 1D array of variable-length strings"
        )
    return v


def check_string_2d(v: np.ndarray) -> np.ndarray:
    if not (
        v.ndim == 2
        and v.dtype == object
        and all(isinstance(x, (str, bytes)) for x in v.flat)
    ):
        raise PydanticCustomError(
            "string_2d_ndarray",
            "Input should be a valid 2D array of variable-length strings"
        )
    return v


NonNegativeInt = Annotated[np.integer, AfterValidator(check_nnint)]
NonNegativeInt1D = Annotated[np.ndarray, AfterValidator(check_nnint_1d)]
Float1D = Annotated[np.ndarray, AfterValidator(check_float_1d)]
Float2D = Annotated[np.ndarray, AfterValidator(check_float_2d)]
String1D = Annotated[np.ndarray, AfterValidator(check_string_1d)]
String2D = Annotated[np.ndarray, AfterValidator(check_string_2d)]


# ======================================================================================
# HDF5 HELPERS
# ======================================================================================
def load_snirf_group(group, group_name):
    """
    Recursively loads a SNIRF HDF5 group into a Pydantic dictionary.
    """
    result = {}

    for name, item in group.items():
        if isinstance(item, h5py.Dataset):
            result[name] = item[()]
        elif isinstance(item, h5py.Group):
            result[name] = load_snirf_group(item, name)

    # Sort by keys
    result = dict(sorted(result.items()))

    # Group indexed groups with valid prefixes
    if "stim" not in group_name:  # avoid grouping stim.data
        for valid_indexed_prefix in RECOGNIZED_INDEXED_PREFIXES:
            pattern = rf"^{re.escape(valid_indexed_prefix)}(\d+)?$"
            indexed_keys = [k for k in result.keys() if re.match(pattern, k)]
            if indexed_keys:
                indexed_items = [result[key] for key in indexed_keys]
                # Remove items with indexed names
                for key in indexed_keys:
                    del result[key]
                # Add new item with a list of indexed groups
                result[valid_indexed_prefix] = indexed_items

    return result


def create_snirf_group(group, data):
    """
    Recursively creates an SNIRF HDF5 group from a Pydantic dictionary.
    """
    for key, value in data.items():
        if value is None:
            continue

        # Handle indexed prefixes
        if isinstance(value, list) and key in RECOGNIZED_INDEXED_PREFIXES:
            for idx, item in enumerate(value):
                subgroup = group.create_group(f"{key}{idx+1}")
                create_snirf_group(subgroup, item)
            continue

        if isinstance(value, dict):
            subgroup = group.create_group(key)
            create_snirf_group(subgroup, value)
        elif isinstance(value, str):
            group.create_dataset(key, data=value.encode('utf-8'))
        else:
            group.create_dataset(key, data=value)


# ======================================================================================
# PYDANTIC HELPERS
# ======================================================================================
class ValidationInfoReport:
    def __init__(self):
        self.warnings: list[str] = []

    def add_warning(self, message: str) -> None:
        self.warnings.append(message)

    def print_warnings(self) -> None:
        if self.warnings:
            print(
                f"{ORANGE}{len(self.warnings)} validation",
                f"warning{'s' if len(self.warnings) > 1 else ''}",
                f"for SNIRFModel{RESET}"
            )
            for warning in self.warnings:
                print(f"{ORANGE}  {warning}{RESET}")


class BaseModelAllowExtra(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True, extra="allow", strict=True
    )


class BaseModelWarnExtra(BaseModelAllowExtra):
    @model_validator(mode="before")
    @classmethod
    def warn_extra_fields(cls, data: Any, info: ValidationInfo) -> Any:
        report = info.context.get("report")
        extra_fields = set(data) - set(cls.model_fields)
        if extra_fields:
            report.add_warning(
                f"Extra fields present in {cls.__name__} ({', '.join(extra_fields)})"
            )
        return data


# ======================================================================================
# SNIRF SCHEMA
# ======================================================================================
# LEVEL 0 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class SNIRFModel(BaseModelWarnExtra):
    formatVersion: str | bytes
    nirs: list[Nirs]  # indexed

    def save(self, file_path: str) -> None:
        """
        Save a SNIRFModel as HDF5.

        Parameters
        ----------
        file_path : str
            Path of the file to which the data is saved.
        """
        data = self.model_dump(exclude_unset=True)
        with h5py.File(file_path, 'w') as f:
            f.attrs['formatVersion'] = data['formatVersion']
            create_snirf_group(f, data)


# LEVEL -1 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Nirs(BaseModelWarnExtra):
    metaDataTags: MetaDataTags  # simple
    data: list[Data]  # indexed
    stim: Optional[list[Stim]] = None  # indexed
    probe: Probe  # simple
    aux: Optional[list[Aux]] = None  # indexed

    # sourceIndex matches sourceLabels
    @model_validator(mode='after')
    def match_sourceindex_sourcelabels(self) -> "Nirs":
        for dat in self.data:
            if dat.measurementLists is not None:
                source_indices = dat.measurementLists.sourceIndex
            elif dat.measurementList is not None:
                source_indices = [ml.sourceIndex for ml in dat.measurementList]
            if np.max(source_indices) > self.probe.sourceLabels.shape[0]:
                raise PydanticCustomError(
                    "conflicting",
                    "Field sourceIndex and sourceLabels should match"
                )
        return self

    # sourceIndex matches sourcePos2D/sourcePos3D
    @model_validator(mode='after')
    def match_sourceindex_sourcepos(self) -> "Nirs":
        for dat in self.data:
            if dat.measurementLists is not None:
                source_indices = dat.measurementLists.sourceIndex
            elif dat.measurementList is not None:
                source_indices = [ml.sourceIndex for ml in dat.measurementList]
            if self.probe.sourcePos2D is not None:
                if np.max(source_indices) > self.probe.sourcePos2D.shape[0]:
                    raise PydanticCustomError(
                        "conflicting",
                        "Field sourceIndex and sourcePos2D should match"
                    )
            if self.probe.sourcePos3D is not None:
                if np.max(source_indices) > self.probe.sourcePos3D.shape[0]:
                    raise PydanticCustomError(
                        "conflicting",
                        "Field sourceIndex and sourcePos3D should match"
                    )
        return self

    # detectorIndex matches detectorLabels
    @model_validator(mode='after')
    def match_detectorindex_detectorlabels(self) -> "Nirs":
        for dat in self.data:
            if dat.measurementLists is not None:
                detector_indices = dat.measurementLists.detectorIndex
            elif dat.measurementList is not None:
                detector_indices = [ml.detectorIndex for ml in dat.measurementList]
            if np.max(detector_indices) > self.probe.detectorLabels.shape[0]:
                raise PydanticCustomError(
                    "conflicting",
                    "Field detectorIndex and detectorLabels should match"
                )
        return self

    # detectorIndex matches detectorPos2D/detectorPos3D
    @model_validator(mode='after')
    def match_detectorindex_detectorpos(self) -> "Nirs":
        for dat in self.data:
            if dat.measurementLists is not None:
                detector_indices = dat.measurementLists.detectorIndex
            elif dat.measurementList is not None:
                detector_indices = [ml.detectorIndex for ml in dat.measurementList]
            if self.probe.detectorPos2D is not None:
                if np.max(detector_indices) > self.probe.detectorPos2D.shape[0]:
                    raise PydanticCustomError(
                        "conflicting",
                        "Field detectorIndex and detectorPos2D should match"
                    )
            if self.probe.detectorPos3D is not None:
                if np.max(detector_indices) > self.probe.detectorPos3D.shape[0]:
                    raise PydanticCustomError(
                        "conflicting",
                        "Field detectorIndex and detectorPos3D should match"
                    )
        return self

    # wavelengthIndex matches wavelengths
    @model_validator(mode='after')
    def match_wavelengthindex_wavelengths(self) -> "Nirs":
        for dat in self.data:
            if dat.measurementLists is not None:
                wavelength_indices = dat.measurementLists.wavelengthIndex
            elif dat.measurementList is not None:
                wavelength_indices = [ml.wavelengthIndex for ml in dat.measurementList]
            if np.max(wavelength_indices) > self.probe.wavelengths.shape[0]:
                raise PydanticCustomError(
                    "conflicting",
                    "Field wavelengthIndex and wavelengths should match"
                )
        return self


# LEVEL -2 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class MetaDataTags(BaseModelAllowExtra):
    SubjectID: str | bytes
    MeasurementDate: str | bytes
    MeasurementTime: str | bytes
    LengthUnit: str | bytes
    TimeUnit: str | bytes
    FrequencyUnit: str | bytes


class Data(BaseModelWarnExtra):
    dataTimeSeries: Float2D
    time: Float1D
    dataOffset: Optional[Float1D] = None
    measurementList: Optional[list[MeasurementList]] = None  # indexed
    measurementLists: Optional[MeasurementLists] = None  # simple

    # measurementList XOR measurementLists
    @model_validator(mode='after')
    def require_measurementlist_xor_measurementlists(self) -> "Data":
        if (
            self.measurementList is not None
            and
            self.measurementLists is not None
        ):
            raise PydanticCustomError(
                "conflicting",
                "Field measurementList and measurementLists cannot both be present"
            )
        if self.measurementList is None and self.measurementLists is None:
            raise PydanticCustomError(
                "missing",
                "One of measurementList or measurementLists is required"
            )
        return self

    # dataTimeSeries matches measurementList
    @model_validator(mode='after')
    def match_datatimeseries_measurementlist(self) -> "Data":
        if self.measurementList is not None:
            if len(self.measurementList) != self.dataTimeSeries.shape[1]:
                raise PydanticCustomError(
                    "conflicting",
                    "Field dataTimeSeries and measurementList should match"
                )
        return self

    # dataTimeSeries matches measurementLists
    @model_validator(mode='after')
    def match_datatimeseries_measurementlists(self) -> "Data":
        if self.measurementLists is not None:
            ml_shapes = [
                item.shape[0]
                for item
                in self.measurementLists.model_dump(exclude_unset=True).values()
            ]
            if not all(s == self.dataTimeSeries.shape[1] for s in ml_shapes):
                raise PydanticCustomError(
                    "conflicting",
                    "Field dataTimeSeries and measurementLists should match"
                )
        return self

    # dataTimeSeries matches dataOffset
    @model_validator(mode='after')
    def match_datatimeseries_dataoffset(self) -> "Data":
        if self.dataOffset is not None:
            if self.dataOffset.shape[0] != self.dataTimeSeries.shape[1]:
                raise PydanticCustomError(
                    "conflicting",
                    "Field dataTimeSeries and dataOffset should match"
                )
        return self

    # dataTimeSeries matches time
    @model_validator(mode='after')
    def match_datatimeseries_time(self) -> "Data":
        if self.time.shape[0] != 2:
            if self.time.shape[0] != self.dataTimeSeries.shape[0]:
                raise PydanticCustomError(
                    "conflicting",
                    "Field dataTimeSeries and time should match"
                )
        return self


class Stim(BaseModelWarnExtra):
    name: str | bytes
    data: Float2D
    dataLabels: Optional[String1D] = None

    # data has at least 3 columns
    @field_validator("data")
    @classmethod
    def check_shape_data(cls, v: Float2D) -> Float2D:
        if v.shape[1] < 3:
            raise PydanticCustomError(
                "shape",
                "Field data should have at least 3 columns"
            )
        return v

    # dataLabels matches data
    @model_validator(mode='after')
    def match_datalabels_data(self) -> "Stim":
        if self.dataLabels is not None:
            if self.data.shape[1] != self.dataLabels.shape[0]:
                raise PydanticCustomError(
                    "conflicting",
                    "Field dataLabels and data should match"
                )
        return self


class Probe(BaseModelWarnExtra):
    wavelengths: Float1D
    wavelengthsEmission: Optional[Float1D] = None
    sourcePos2D: Optional[Float2D] = None
    sourcePos3D: Optional[Float2D] = None
    detectorPos2D: Optional[Float2D] = None
    detectorPos3D: Optional[Float2D] = None
    frequencies: Optional[Float1D] = None
    timeDelays: Optional[Float1D] = None
    timeDelayWidths: Optional[Float1D] = None
    momentOrders: Optional[Float1D] = None
    correlationTimeDelays: Optional[Float1D] = None
    correlationTimeDelayWidths: Optional[Float1D] = None
    sourceLabels: Optional[String2D] = None  # FIXME
    detectorLabels: Optional[String1D] = None
    landmarkPos2D: Optional[Float2D] = None
    landmarkPos3D: Optional[Float2D] = None
    landmarkLabels: Optional[String1D] = None
    coordinateSystem: Optional[str | bytes] = None
    coordinateSystemDescription: Optional[str | bytes] = None

    # sourcePos2D OR sourcePos3D
    @model_validator(mode='after')
    def require_sourcepos2d_or_sourcepos3d(self) -> "Probe":
        if self.sourcePos2D is None and self.sourcePos3D is None:
            raise PydanticCustomError(
                "missing",
                "At least one of sourcePos2D or sourcePos3D is required"
            )
        return self

    # detectorPos2D OR detectorPos3D
    @model_validator(mode='after')
    def require_detectorpos2d_or_detectorpos3d(self) -> "Probe":
        if self.detectorPos2D is None and self.detectorPos3D is None:
            raise PydanticCustomError(
                "missing",
                "At least one of detectorPos2D or detectorPos3D is required"
            )
        return self

    # Warn if unrecognized coordinateSystem
    @model_validator(mode='after')
    def check_coordinatesystem(self, info: ValidationInfo) -> "Probe":
        report = info.context.get("report")
        if self.coordinateSystem is not None:
            if self.coordinateSystem.decode() not in RECOGNIZED_COORDINATE_SYSTEMS:
                report.add_warning(
                    "Value of coordinateSystem is not recognized (see Appendix)"
                )
        return self

    # Warn if missing coordinateSystemDescription with unrecognized coordinateSystem
    @model_validator(mode='after')
    def check_coordinatesystemdescription(self, info: ValidationInfo) -> "Probe":
        report = info.context.get("report")
        if self.coordinateSystem is not None:
            if (
                self.coordinateSystem.decode() not in RECOGNIZED_COORDINATE_SYSTEMS
                and self.coordinateSystemDescription is None
            ):
                report.add_warning(
                    "Field coordinateSystemDescription is required if "
                    "coordinateSystem is not recognized"
                )
        return self


class Aux(BaseModelWarnExtra):
    name: str | bytes
    dataTimeSeries: Float2D
    dataUnit: Optional[str | bytes] = None
    time: Float1D
    timeOffset: Optional[Float1D] = None


# LEVEL -3 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class MeasurementList(BaseModelWarnExtra):
    sourceIndex: NonNegativeInt
    detectorIndex: NonNegativeInt
    wavelengthIndex: NonNegativeInt
    wavelengthActual: Optional[float | np.floating] = None
    wavelengthEmissionActual: Optional[float | np.floating] = None
    dataType: NonNegativeInt
    dataUnit: Optional[str | bytes] = None
    dataTypeLabel: Optional[str | bytes] = None
    dataTypeIndex: NonNegativeInt
    sourcePower: Optional[float | np.floating] = None
    detectorGain: Optional[float | np.floating] = None

    # Warn if null index
    @field_validator("sourceIndex", "detectorIndex", "wavelengthIndex", "dataTypeIndex")
    @classmethod
    def check_non_null(
        cls, v: NonNegativeInt, info: ValidationInfo
    ) -> NonNegativeInt:
        report = info.context.get("report")
        if v == 0:
            report.add_warning(
                f"An index of zero in {info.field_name} is usually undefined"
            )
        return v

    # Warn if unrecognized dataTypeLabel
    @field_validator("dataTypeLabel")
    @classmethod
    def check_recognized_datatypelabel(
        cls, v: str | bytes, info: ValidationInfo
    ) -> str | bytes:
        report = info.context.get("report")
        if v.decode() not in RECOGNIZED_DATA_TYPE_LABELS:
            report.add_warning(
                f"Value of {info.field_name} is not recognized (see Appendix)"
            )
        return v

    # Warn if unrecognized dataType
    @field_validator("dataType")
    @classmethod
    def check_recognized_datatype(
        cls, v: NonNegativeInt, info: ValidationInfo
    ) -> NonNegativeInt:
        report = info.context.get("report")
        if v not in RECOGNIZED_DATA_TYPES:
            report.add_warning(
                f"Value of {info.field_name} is not recognized (see Appendix)"
            )
        return v

    # dataTypeLabel IF dataType 99999
    @model_validator(mode='after')
    def require_datatypelabel(self) -> "MeasurementList":
        if self.dataType == 99999 and self.dataTypeLabel is None:
            raise PydanticCustomError(
                "missing",
                "Field dataTypeLabel is required when dataType is 99999"
            )
        return self


class MeasurementLists(BaseModelWarnExtra):
    sourceIndex: NonNegativeInt1D
    detectorIndex: NonNegativeInt1D
    wavelengthIndex: NonNegativeInt1D
    wavelengthActual: Optional[Float1D] = None
    wavelengthEmissionActual: Optional[Float1D] = None
    dataType: NonNegativeInt1D
    dataUnit: Optional[String1D] = None
    dataTypeLabel: Optional[String1D] = None
    dataTypeIndex: NonNegativeInt1D
    sourcePower: Optional[Float1D] = None
    detectorGain: Optional[Float1D] = None

    # Warn if null index
    @field_validator("sourceIndex", "detectorIndex", "wavelengthIndex", "dataTypeIndex")
    @classmethod
    def check_non_null(
        cls, v: NonNegativeInt1D, info: ValidationInfo
    ) -> NonNegativeInt1D:
        report = info.context.get("report")
        if np.any(v == 0):
            report.add_warning(
                f"An index of zero in {info.field_name} is usually undefined"
            )
        return v

    # Warn if unrecognized dataTypeLabel
    @field_validator("dataTypeLabel")
    @classmethod
    def check_recognized_datatypelabel(
        cls, v: String1D, info: ValidationInfo
    ) -> String1D:
        report = info.context.get("report")
        v_str = np.array([s.decode() for s in v])
        if np.any(~np.isin(v_str, RECOGNIZED_DATA_TYPE_LABELS)):
            report.add_warning(
                f"Value of {info.field_name} is not recognized (see Appendix)"
            )
        return v

    # Warn if unrecognized dataType
    @field_validator("dataType")
    @classmethod
    def check_recognized_datatype(
        cls, v: NonNegativeInt1D, info: ValidationInfo
    ) -> NonNegativeInt1D:
        report = info.context.get("report")
        if np.any(~np.isin(v, RECOGNIZED_DATA_TYPES)):
            report.add_warning(
                f"Value of {info.field_name} is not recognized (see Appendix)"
            )
        return v

    # dataTypeLabel IF dataType 99999
    @model_validator(mode='after')
    def require_datatypelabel(self) -> "MeasurementLists":
        if np.any(self.dataType == 99999) and self.dataTypeLabel is None:
            raise PydanticCustomError(
                "missing",
                "Field dataTypeLabel is required when dataType is 99999"
            )
        return self


# ======================================================================================
# SNIRF READER
# ======================================================================================
def read_snirf(file_path, verbose=False):
    """
    Read a SNIRF file, logging potential errors and warnings.

    Parameters
    ----------
    file_path : str
        Path of the SNIRF file to load.

    verbose : bool
        Whether to print validation info. Defaults to ``False``.

    Returns
    -------
    snirf : SNIRFModel
        The loaded SNIRF Pydantic model object.
    """
    snirf = None

    if not file_path.endswith('.snirf'):
        print(f"{RED}ERROR: Valid SNIRF files must end with .snirf{RESET}")

    else:
        report = ValidationInfoReport()
        with h5py.File(file_path, "r") as f:
            data = load_snirf_group(f, os.path.basename(file_path))
        try:
            snirf = SNIRFModel.model_validate(data, context={"report": report})
        except ValidationError as e:
            print(f"{RED}{e}{RESET}")
        finally:
            if verbose is True:
                if snirf is not None:
                    print(f"{GREEN}Valid SNIRFModel{RESET}")
                report.print_warnings()

    return snirf


# ======================================================================================
# MAIN (SNIRF VALIDATOR)
# ======================================================================================
def main():
    import argparse
    print("===============")
    print("SNIRF VALIDATOR")
    print("---------------")
    parser = argparse.ArgumentParser(description='Validate a SNIRF file.')
    parser.add_argument('filename', type=str, help='Path to the SNIRF file')
    args = parser.parse_args()
    read_snirf(args.filename, verbose=True)


if __name__ == "__main__":
    main()
