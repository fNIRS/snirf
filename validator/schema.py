from __future__ import annotations

import numpy as np
from pydantic import BaseModel, ConfigDict, model_validator, AfterValidator
from typing import Optional, List, Annotated


# TODO:
# - [x] structure of variables (names and nesting)
# - [x] types
# - [x] required and optional conditionals
# - [ ] formatting of variables (dimensions and shape matching)
# - [ ] HDF5 to Pydantic


# =============================================================================
# HELPERS
# =============================================================================
def check_int_1d(v: np.ndarray) -> bool:
    if not (v.ndim == 1 and np.issubdtype(v.dtype, np.integer)):
        raise ValueError("expected a 1D array of integers")
    return v


def check_float_1d(v: np.ndarray) -> bool:
    if not (v.ndim == 1 and np.issubdtype(v.dtype, np.floating)):
        raise ValueError("expected a 1D array of floats")
    return v


def check_float_2d(v: np.ndarray) -> bool:
    if not (v.ndim == 2 and np.issubdtype(v.dtype, np.floating)):
        raise ValueError("expected a 2D array of floats")
    return v


def check_string_1d(v: np.ndarray) -> bool:
    if v.ndim != 1:
        raise ValueError("expected a 1D array of strings")
    if not np.issubdtype(v.dtype, np.character):
        raise ValueError("expected a 1D array of strings")
    if v.dtype == object:
        if not all(isinstance(x, str) for x in v.flat):
            raise ValueError("expected a 1D array of strings")
    return v


def check_string_2d(v: np.ndarray) -> bool:
    if v.ndim != 2:
        raise ValueError("expected a 2D array of strings")
    if not np.issubdtype(v.dtype, np.character):
        raise ValueError("expected a 2D array of strings")
    if v.dtype == object:
        if not all(isinstance(x, str) for x in v.flat):
            raise ValueError("expected a 2D array of strings")
    return v


Integer1D = Annotated[np.ndarray, AfterValidator(check_int_1d)]
Float1D = Annotated[np.ndarray, AfterValidator(check_float_1d)]
Float2D = Annotated[np.ndarray, AfterValidator(check_float_2d)]
String1D = Annotated[np.ndarray, AfterValidator(check_string_1d)]
String2D = Annotated[np.ndarray, AfterValidator(check_string_2d)]


# =============================================================================
# SNIRF PYDANTIC SCHEMA
# =============================================================================
# LEVEL 0 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class SNIRFFile(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    formatVersion: str
    nirs: List[Nirs]  # TODO: indexed HDF5 group


# LEVEL -1 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Nirs(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    metaDataTags: MetaDataTags  # TODO: simple HDF5 group
    data: List[Data]  # TODO: indexed HDF5 group
    stim: Optional[List[Stim]] = None  # TODO: indexed HDF5 group
    probe: Probe  # TODO: simple HDF5 group
    aux: Optional[List[Aux]] = None  # TODO: indexed HDF5 group


# LEVEL -2 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class MetaDataTags(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    SubjectID: str
    MeasurementDate: str
    MeasurementTime: str
    LengthUnit: str
    TimeUnit: str
    FrequencyUnit: str

    # Additional user-defined metadata entries
    model_config = ConfigDict(extra="allow")


class Data(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    dataTimeSeries: Float2D
    time: Float1D
    dataOffset: Optional[Float1D] = None
    measurementList: Optional[List[MeasurementList]] = None  # TODO: indexed HDF5 group
    measurementLists: Optional[MeasurementLists] = None  # TODO: simple HDF5 group

    @model_validator(mode='after')
    def require_measurementlist_xor_measurementlists(self) -> "Data":
        if self.measurementList and self.measurementLists:
            raise ValueError(
                "'measurementList' and 'measurementLists' cannot both be "
                "present"
            )
        if not self.measurementList and not self.measurementLists:
            raise ValueError(
                "either 'measurementList' or 'measurementLists' is required"
            )
        return self


class Stim(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    name: str
    data: Float2D
    dataLabels: Optional[String1D] = None


class Probe(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
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
    sourceLabels: Optional[String2D] = None
    detectorLabels: Optional[String1D] = None
    landmarkPos2D: Optional[Float2D] = None
    landmarkPos3D: Optional[Float2D] = None
    landmarkLabels: Optional[String1D] = None
    coordinateSystem: Optional[str] = None
    coordinateSystemDescription: Optional[str] = None

    @model_validator(mode='after')
    def require_sourcepos2d_or_sourcepos3d(self) -> "Probe":
        if not self.sourcePos2D and not self.sourcePos3D:
            raise ValueError(
                "at least one of sourcePos2D or sourcePos3D is required"
            )
        return self

    @model_validator(mode='after')
    def require_detectorpos2d_or_detectorpos3d(self) -> "Probe":
        if not self.detectorPos2D and not self.detectorPos3D:
            raise ValueError(
                "at least one of detectorPos2D or detectorPos3D is required"
            )
        return self


class Aux(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    name: str
    dataTimeSeries: Float2D
    dataUnit: Optional[str] = None
    time: Float1D
    timeOffset: Optional[Float1D] = None


# LEVEL -3 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class MeasurementList(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    sourceIndex: int
    detectorIndex: int
    wavelengthIndex: int
    wavelengthActual: Optional[float] = None
    wavelengthEmissionActual: Optional[float] = None
    dataType: int
    dataUnit: Optional[str] = None
    dataTypeLabel: Optional[str] = None
    dataTypeIndex: int
    sourcePower: Optional[float] = None
    detectorGain: Optional[float] = None


class MeasurementLists(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    sourceIndex: Integer1D
    detectorIndex: Integer1D
    wavelengthIndex: Integer1D
    wavelengthActual: Optional[Float1D] = None
    wavelengthEmissionActual: Optional[Float1D] = None
    dataType: Integer1D
    dataUnit: Optional[String1D] = None
    dataTypeLabel: Optional[String1D] = None
    dataTypeIndex: Integer1D
    sourcePower: Optional[Float1D] = None
    detectorGain: Optional[Float1D] = None


# =============================================================================
# TESTING
# =============================================================================
import h5py

f = h5py.File('sub-01_task-tapping_nirs.snirf', 'r')
print(f.keys())
