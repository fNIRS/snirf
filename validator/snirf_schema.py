from __future__ import annotations

import numpy as np
import os

from pydantic import (BaseModel, ConfigDict, AfterValidator, ValidationInfo,
                      model_validator, field_validator)
from pydantic_core import PydanticCustomError
from typing import Optional, List, Annotated

os.environ['PYDANTIC_ERRORS_INCLUDE_URL'] = 'false'
RECOGNIZED_INDEXED_PREFIXES = [
    'nirs',
    'data',
    'stim',
    'aux',
    'measurementList'
]
RECOGNIZED_COORDINATE_SYSTEM_NAMES = [
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
RECOGNIZED_AUX_NAMES = [
    'ACCEL_X',
    'ACCEL_Y',
    'ACCEL_Z',
    'GYRO_X',
    'GYRO_Y',
    'GYRO_Z',
    'MAGN_X',
    'MAGN_Y',
    'MAGN_Z',
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

ORANGE = '\033[33m'
RESET = '\033[0m'


# =============================================================================
# TYPE HELPERS
# =============================================================================
def check_nnint(v: int | np.integer) -> int | np.integer:
    if v < 0:
        raise PydanticCustomError(
            "nnint_type",
            "Input should be a valid integer greater than or equal to 0"
        )
    return v


def check_nnint_1d(v: np.ndarray) -> np.ndarray:
    if not (v.ndim == 1 and np.issubdtype(v.dtype, np.integer) and np.all(v >= 0)):
        raise PydanticCustomError(
            "nnint_1d_ndarray",
            "Input should be a valid 1D array of integers greater than or equal to 0"
        )
    return v


def check_float_1d(v: np.ndarray) -> np.ndarray:
    if not (v.ndim == 1 and np.issubdtype(v.dtype, np.floating)):
        raise PydanticCustomError(
            "float_1d_ndarray",
            "Input should be a valid 1D array of floats"
        )
    return v


def check_float_2d(v: np.ndarray) -> np.ndarray:
    if not (v.ndim == 2 and np.issubdtype(v.dtype, np.floating)):
        raise PydanticCustomError(
            "float_2d_ndarray",
            "Input should be a valid 2D array of floats"
        )
    return v


def check_string_1d(v: np.ndarray) -> np.ndarray:
    if not (v.ndim == 1 and v.dtype == object):
        raise PydanticCustomError(
            "string_1d_ndarray",
            "Input should be a valid 1D array of variable-length strings"
        )
    if not all(isinstance(x, (str, bytes)) for x in v.flat):
        raise PydanticCustomError(
            "string_1d_ndarray",
            "Input should be a valid 1D array of variable-length strings"
        )
    return v


def check_string_2d(v: np.ndarray) -> np.ndarray:
    if not (v.ndim == 2 and v.dtype == object):
        raise PydanticCustomError(
            "string_2d_ndarray",
            "Input should be a valid 2D array of variable-length strings"
        )
    if not all(isinstance(x, (str, bytes)) for x in v.flat):
        raise PydanticCustomError(
            "string_2d_ndarray",
            "Input should be a valid 2D array of variable-length strings"
        )
    return v


NonNegativeInt = Annotated[int | np.integer, AfterValidator(check_nnint)]
NonNegativeInt1D = Annotated[np.ndarray, AfterValidator(check_nnint_1d)]
Float1D = Annotated[np.ndarray, AfterValidator(check_float_1d)]
Float2D = Annotated[np.ndarray, AfterValidator(check_float_2d)]
String1D = Annotated[np.ndarray, AfterValidator(check_string_1d)]
String2D = Annotated[np.ndarray, AfterValidator(check_string_2d)]


# =============================================================================
# SCHEMA CONFIGS
# =============================================================================
class BaseModelAllowExtra(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, extra="allow",
                              strict=True)


class BaseModelWarnExtra(BaseModelAllowExtra):
    @model_validator(mode="after")
    def warn_extra_fields(self):
        if self.__pydantic_extra__:
            extra_fields = list(self.__pydantic_extra__.keys())
            print(
                f"{ORANGE}WARNING: Extra fields present in",
                f"{type(self).__name__}",
                f"({', '.join(extra_fields)}){RESET}"
            )
        return self


# =============================================================================
# SNIRF SCHEMA
# =============================================================================
# LEVEL 0 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class SNIRFFile(BaseModelWarnExtra):
    formatVersion: str | bytes
    nirs: List[Nirs]  # indexed


# LEVEL -1 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Nirs(BaseModelWarnExtra):
    metaDataTags: MetaDataTags  # simple
    data: List[Data]  # indexed
    stim: Optional[List[Stim]] = None  # indexed
    probe: Probe  # simple
    aux: Optional[List[Aux]] = None  # indexed

    # Matching sourceIndex
    @model_validator(mode='after')
    def match_sourceindex(self) -> "Nirs":
        for dat in self.data:
            if dat.measurementLists is not None:
                source_indices = dat.measurementLists.sourceIndex
            elif dat.measurementList is not None:
                source_indices = [
                    ml.sourceIndex for ml in dat.measurementList
                ]
            if np.max(source_indices) > self.probe.sourceLabels.shape[0]:
                raise PydanticCustomError(
                    "conflicting",
                    "Field sourceIndex and sourceLabels should match"
                )
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

    # Matching detectorIndex
    @model_validator(mode='after')
    def match_detectorindex(self) -> "Nirs":
        for dat in self.data:
            if dat.measurementLists is not None:
                detector_indices = dat.measurementLists.detectorIndex
            elif dat.measurementList is not None:
                detector_indices = [
                    ml.detectorIndex for ml in dat.measurementList
                ]
            if np.max(detector_indices) > self.probe.detectorLabels.shape[0]:
                raise PydanticCustomError(
                    "conflicting",
                    "Field detectorIndex and detectorLabels should match"
                )
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

    # Matching wavelengthIndex
    @model_validator(mode='after')
    def match_wavelengthindex(self) -> "Nirs":
        for dat in self.data:
            if dat.measurementLists is not None:
                wavelength_indices = dat.measurementLists.wavelengthIndex
            elif dat.measurementList is not None:
                wavelength_indices = [
                    ml.wavelengthIndex for ml in dat.measurementList
                ]
            if np.max(wavelength_indices) > self.probe.wavelengths.shape[0]:
                raise PydanticCustomError(
                    "conflicting",
                    "Field wavelengthIndex and wavelengths should match"
                )

        return self


# LEVEL -2 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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
    measurementList: Optional[List[MeasurementList]] = None  # indexed
    measurementLists: Optional[MeasurementLists] = None  # simple

    # MeasurementList XOR MeasurementLists
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
                "Strictly one of measurementList or measurementLists is required"
            )
        return self

    # Matching dataTimeSeries and measurementList
    @model_validator(mode='after')
    def match_datatimeseries_measurementlist(self) -> "Data":
        if self.measurementList is not None:
            if len(self.measurementList) != self.dataTimeSeries.shape[1]:
                raise PydanticCustomError(
                    "conflicting",
                    "Field dataTimeSeries and measurementList should match"
                )
        return self

    # Matching dataTimeSeries and measurementLists
    @model_validator(mode='after')
    def match_datatimeseries_measurementlists(self) -> "Data":
        if self.measurementLists is not None:
            ml_shapes = [
                item.shape[0]
                for item in self.measurementLists.model_dump().values()
            ]
            if not all(s == self.dataTimeSeries.shape[1] for s in ml_shapes):
                raise PydanticCustomError(
                    "conflicting",
                    "Field dataTimeSeries and measurementLists should match"
                )
        return self

    # Matching dataTimeSeries and dataOffset
    @model_validator(mode='after')
    def match_datatimeseries_dataoffset(self) -> "Data":
        if self.dataOffset is not None:
            if self.dataOffset.shape[0] != self.dataTimeSeries.shape[1]:
                raise PydanticCustomError(
                    "conflicting",
                    "Field dataTimeSeries and dataOffset should match"
                )
        return self

    # Matching dataTimeSeries and time
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

    # Matching dataLabels and data
    @model_validator(mode='after')
    def match_datalabels_data(self) -> "Stim":
        if self.dataLabels is not None:
            if self.data.shape[0] != self.dataLabels.shape[0]:
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


class Aux(BaseModelWarnExtra):
    name: str | bytes
    dataTimeSeries: Float2D
    dataUnit: Optional[str | bytes] = None
    time: Float1D
    timeOffset: Optional[Float1D] = None


# LEVEL -3 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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
    @field_validator(
        "sourceIndex", "detectorIndex", "wavelengthIndex", "dataTypeIndex"
    )
    @classmethod
    def check_non_null(
        cls, v: NonNegativeInt, info: ValidationInfo
    ) -> NonNegativeInt:
        if v == 0:
            print(
                f"{ORANGE}WARNING: An index of zero in {info.field_name}",
                f"is usually undefined{RESET}",
            )
        return v

    # Warn if unrecognized dataTypeLabel
    @field_validator("dataTypeLabel")
    @classmethod
    def check_recognized_datatypelabel(
        cls, v: str | bytes, info: ValidationInfo
    ) -> str | bytes:
        if v not in RECOGNIZED_DATA_TYPE_LABELS:
            print(
                f"{ORANGE}WARNING: Value of {info.field_name} is not",
                f"recognized (see Appendix){RESET}",
            )
        return v

    # Warn if unrecognized dataType
    @field_validator("dataType")
    @classmethod
    def check_recognized_datatype(
        cls, v: NonNegativeInt, info: ValidationInfo
    ) -> NonNegativeInt:
        if v not in RECOGNIZED_DATA_TYPES:
            print(
                f"{ORANGE}WARNING: Value of {info.field_name} is not",
                f"recognized (see Appendix){RESET}",
            )
        return v


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
    @field_validator(
        "sourceIndex", "detectorIndex", "wavelengthIndex", "dataTypeIndex"
    )
    @classmethod
    def check_non_null(
        cls, v: NonNegativeInt1D, info: ValidationInfo
    ) -> NonNegativeInt1D:
        if np.any(v == 0):
            print(
                f"{ORANGE}WARNING: An index of zero in {info.field_name}",
                f"is usually undefined{RESET}",
            )
        return v

    # Warn if unrecognized dataTypeLabel
    @field_validator("dataTypeLabel")
    @classmethod
    def check_recognized_datatypelabel(
        cls, v: String1D, info: ValidationInfo
    ) -> String1D:
        if np.any(~np.isin(v, RECOGNIZED_DATA_TYPE_LABELS)):
            print(
                f"{ORANGE}WARNING: Value of {info.field_name} is not",
                f"recognized (see Appendix){RESET}",
            )
        return v

    # Warn if unrecognized dataType
    @field_validator("dataType")
    @classmethod
    def check_recognized_datatype(
        cls, v: NonNegativeInt1D, info: ValidationInfo
    ) -> NonNegativeInt1D:
        if np.any(~np.isin(v, RECOGNIZED_DATA_TYPES)):
            print(
                f"{ORANGE}WARNING: Value of {info.field_name} is not",
                f"recognized (see Appendix){RESET}",
            )
        return v
