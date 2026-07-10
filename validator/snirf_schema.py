from __future__ import annotations

import numpy as np
import os

from pydantic import BaseModel, ConfigDict, model_validator, AfterValidator
from pydantic_core import PydanticCustomError
from typing import Optional, List, Annotated

os.environ['PYDANTIC_ERRORS_INCLUDE_URL'] = 'false'
VALID_INDEXED_PREFIXES = ['nirs', 'data', 'stim', 'aux', 'measurementList']


# =============================================================================
# HELPERS
# =============================================================================
def check_int_1d(v: np.ndarray) -> np.ndarray:
    if not (v.ndim == 1 and np.issubdtype(v.dtype, int)):
        raise PydanticCustomError(
            "int_1d_ndarray",
            "Input should be a valid 1D array of integers"
        )
    return v


def check_float_1d(v: np.ndarray) -> np.ndarray:
    if not (v.ndim == 1 and np.issubdtype(v.dtype, float)):
        raise PydanticCustomError(
            "float_1d_ndarray",
            "Input should be a valid 1D array of floats"
        )
    return v


def check_float_2d(v: np.ndarray) -> np.ndarray:
    if not (v.ndim == 2 and np.issubdtype(v.dtype, float)):
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


Integer1D = Annotated[np.ndarray, AfterValidator(check_int_1d)]
Float1D = Annotated[np.ndarray, AfterValidator(check_float_1d)]
Float2D = Annotated[np.ndarray, AfterValidator(check_float_2d)]
String1D = Annotated[np.ndarray, AfterValidator(check_string_1d)]
String2D = Annotated[np.ndarray, AfterValidator(check_string_2d)]


class BaseModelAllowExtra(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, extra="allow")


class BaseModelWarnExtra(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, extra="allow")

    @model_validator(mode="after")
    def log_extra_fields(self):
        if self.__pydantic_extra__:
            print(
                f"{'\033[33m'}WARNING: Extra fields present in",
                f"{type(self).__name__}:",
                f"{list(self.__pydantic_extra__.keys())}{'\033[0m'}"
            )
        return self


# =============================================================================
# SNIRF PYDANTIC SCHEMA
# =============================================================================
# LEVEL 0 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class SNIRFFile(BaseModelWarnExtra):
    formatVersion: str
    nirs: List[Nirs]  # indexed


# LEVEL -1 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Nirs(BaseModelWarnExtra):
    metaDataTags: MetaDataTags  # simple
    data: List[Data]  # indexed
    stim: Optional[List[Stim]] = None  # indexed
    probe: Probe  # simple
    aux: Optional[List[Aux]] = None  # indexed


# LEVEL -2 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class MetaDataTags(BaseModelAllowExtra):
    SubjectID: str
    MeasurementDate: str
    MeasurementTime: str
    LengthUnit: str
    TimeUnit: str
    FrequencyUnit: str


class Data(BaseModelWarnExtra):
    dataTimeSeries: Float2D
    time: Float1D
    dataOffset: Optional[Float1D] = None
    measurementList: Optional[List[MeasurementList]] = None  # indexed
    measurementLists: Optional[MeasurementLists] = None  # simple

    @model_validator(mode='after')
    def require_measurementlist_xor_measurementlists(self) -> "Data":
        if (
            self.measurementList is not None
            and
            self.measurementLists is not None
        ):
            raise ValueError(
                "'measurementList' and 'measurementLists' cannot both be "
                "present"
            )
        if self.measurementList is None and self.measurementLists is None:
            raise ValueError(
                "either 'measurementList' or 'measurementLists' is required"
            )
        return self


class Stim(BaseModelWarnExtra):
    name: str
    data: Float2D
    dataLabels: Optional[String1D] = None


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
    sourceLabels: Optional[String2D] = None
    detectorLabels: Optional[String1D] = None
    landmarkPos2D: Optional[Float2D] = None
    landmarkPos3D: Optional[Float2D] = None
    landmarkLabels: Optional[String1D] = None
    coordinateSystem: Optional[str] = None
    coordinateSystemDescription: Optional[str] = None

    @model_validator(mode='after')
    def require_sourcepos2d_or_sourcepos3d(self) -> "Probe":
        if self.sourcePos2D is None and self.sourcePos3D is None:
            raise ValueError(
                "at least one of sourcePos2D or sourcePos3D is required"
            )
        return self

    @model_validator(mode='after')
    def require_detectorpos2d_or_detectorpos3d(self) -> "Probe":
        if self.detectorPos2D is None and self.detectorPos3D is None:
            raise ValueError(
                "at least one of detectorPos2D or detectorPos3D is required"
            )
        return self


class Aux(BaseModelWarnExtra):
    name: str
    dataTimeSeries: Float2D
    dataUnit: Optional[str] = None
    time: Float1D
    timeOffset: Optional[Float1D] = None


# LEVEL -3 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class MeasurementList(BaseModelWarnExtra):
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


class MeasurementLists(BaseModelWarnExtra):
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
