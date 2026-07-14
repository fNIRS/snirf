import numpy as np
import warnings
from snirf_schema import (read_snirf,
                          RECOGNIZED_COORDINATE_SYSTEMS,
                          RECOGNIZED_DATA_TYPE_LABELS)

VALID_SNIRF_ML_PATH = "valid_ml.snirf"
VALID_SNIRF_MLS_PATH = "valid_mls.snirf"


# GOOD ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def test_valid_measurementlist(capsys):
    result = read_snirf(VALID_SNIRF_ML_PATH, verbose=True)
    out = capsys.readouterr().out
    assert result is not None and "Valid SNIRFFile" in out
    assert "error" not in out.lower()
    assert "warning" not in out.lower()


def test_valid_measurementlists(capsys):
    result = read_snirf(VALID_SNIRF_MLS_PATH, verbose=True)
    out = capsys.readouterr().out
    assert result is not None and "Valid SNIRFFile" in out
    assert "error" not in out.lower()
    assert "warning" not in out.lower()


# FILE PATH ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def test_invalid_extension(tmp_path, capsys):
    result = read_snirf(VALID_SNIRF_ML_PATH)
    result.save(f"{tmp_path}test.nirs")
    result = read_snirf(f"{tmp_path}test.nirs", verbose=True)
    out = capsys.readouterr().out
    assert result is None and "Valid SNIRFFile" not in out
    assert "ERROR: Valid SNIRF files must end with .snirf" in out


# LEVEL 0 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def test_invalid_type(tmp_path, capsys):
    result = read_snirf(VALID_SNIRF_ML_PATH)
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=UserWarning)
        result.formatVersion = 0.1
        result.save(f"{tmp_path}test.snirf")
    result = read_snirf(f"{tmp_path}test.snirf", verbose=True)
    out = capsys.readouterr().out
    assert result is None and "Valid SNIRFFile" not in out
    assert "\nformatVersion.str\n  Input should be a valid string" in out
    assert "\nformatVersion.bytes\n  Input should be a valid bytes" in out


def test_missing_field(tmp_path, capsys):
    result = read_snirf(VALID_SNIRF_ML_PATH)
    del result.nirs
    result.save(f"{tmp_path}test.snirf")
    result = read_snirf(f"{tmp_path}test.snirf", verbose=True)
    out = capsys.readouterr().out
    assert result is None and "Valid SNIRFFile" not in out
    assert "\nnirs\n  Field required" in out


def test_warn_extra_field(tmp_path, capsys):
    result = read_snirf(VALID_SNIRF_ML_PATH)
    result.extra = "extra"
    result.save(f"{tmp_path}test.snirf")
    result = read_snirf(f"{tmp_path}test.snirf", verbose=True)
    out = capsys.readouterr().out
    assert result is not None and "Valid SNIRFFile" in out
    assert "warning" in out.lower()
    assert "Extra fields present in SNIRFFile" in out


# LEVEL -1 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def test_mismatched_sourceindex_sourcelabels(tmp_path, capsys):
    result = read_snirf(VALID_SNIRF_ML_PATH)
    result.nirs[0].probe.sourceLabels = result.nirs[0].probe.sourceLabels[:-1]
    result.save(f"{tmp_path}test.snirf")
    result = read_snirf(f"{tmp_path}test.snirf", verbose=True)
    out = capsys.readouterr().out
    assert result is None and "Valid SNIRFFile" not in out
    assert "Field sourceIndex and sourceLabels should match" in out


def test_mismatched_sourceindex_sourcepos(tmp_path, capsys):
    result = read_snirf(VALID_SNIRF_ML_PATH)
    result.nirs[0].probe.sourcePos2D = result.nirs[0].probe.sourcePos2D[:-1]
    result.save(f"{tmp_path}test.snirf")
    result = read_snirf(f"{tmp_path}test.snirf", verbose=True)
    out = capsys.readouterr().out
    assert result is None and "Valid SNIRFFile" not in out
    assert "Field sourceIndex and sourcePos2D should match" in out


def test_mismatched_detectorindex_detectorlabels(tmp_path, capsys):
    result = read_snirf(VALID_SNIRF_ML_PATH)
    result.nirs[0].probe.detectorLabels = result.nirs[0].probe.detectorLabels[:-1]
    result.save(f"{tmp_path}test.snirf")
    result = read_snirf(f"{tmp_path}test.snirf", verbose=True)
    out = capsys.readouterr().out
    assert result is None and "Valid SNIRFFile" not in out
    assert "Field detectorIndex and detectorLabels should match" in out


def test_mismatched_detectorindex_detectorpos(tmp_path, capsys):
    result = read_snirf(VALID_SNIRF_ML_PATH)
    result.nirs[0].probe.detectorPos2D = result.nirs[0].probe.detectorPos2D[:-1]
    result.save(f"{tmp_path}test.snirf")
    result = read_snirf(f"{tmp_path}test.snirf", verbose=True)
    out = capsys.readouterr().out
    assert result is None and "Valid SNIRFFile" not in out
    assert "Field detectorIndex and detectorPos2D should match" in out


def test_mismatched_wavelengthindex_wavelengthlabels(tmp_path, capsys):
    result = read_snirf(VALID_SNIRF_ML_PATH)
    result.nirs[0].probe.wavelengths = result.nirs[0].probe.wavelengths[:-1]
    result.save(f"{tmp_path}test.snirf")
    result = read_snirf(f"{tmp_path}test.snirf", verbose=True)
    out = capsys.readouterr().out
    assert result is None and "Valid SNIRFFile" not in out
    assert "Field wavelengthIndex and wavelengths should match" in out


# LEVEL -2 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def test_valid_extra_field(tmp_path, capsys):
    result = read_snirf(VALID_SNIRF_ML_PATH)
    result.nirs[0].metaDataTags.extra = "extra"
    result.save(f"{tmp_path}test.snirf")
    result = read_snirf(f"{tmp_path}test.snirf", verbose=True)
    out = capsys.readouterr().out
    assert result is not None and "Valid SNIRFFile" in out
    assert "error" not in out.lower()
    assert "warning" not in out.lower()


def test_invalid_dim(tmp_path, capsys):
    result = read_snirf(VALID_SNIRF_MLS_PATH)
    result.nirs[0].data[0].dataTimeSeries = result.nirs[0].data[0].dataTimeSeries[:, :, None]
    result.save(f"{tmp_path}test.snirf")
    result = read_snirf(f"{tmp_path}test.snirf", verbose=True)
    out = capsys.readouterr().out
    assert result is None and "Valid SNIRFFile" not in out
    assert "\nnirs.0.data.0.dataTimeSeries\n  Input should be a valid 2D array" in out


def test_measurementlist_measurementlists(tmp_path, capsys):
    result = read_snirf(VALID_SNIRF_ML_PATH)
    mls = read_snirf(VALID_SNIRF_MLS_PATH).nirs[0].data[0].measurementLists
    result.nirs[0].data[0].measurementLists = mls
    result.save(f"{tmp_path}test.snirf")
    result = read_snirf(f"{tmp_path}test.snirf", verbose=True)
    out = capsys.readouterr().out
    assert result is None and "Valid SNIRFFile" not in out
    assert "measurementList and measurementLists cannot both be present" in out


def test_missing_measurementlist_missing_measurementlists(tmp_path, capsys):
    result = read_snirf(VALID_SNIRF_ML_PATH)
    del result.nirs[0].data[0].measurementList
    result.save(f"{tmp_path}test.snirf")
    result = read_snirf(f"{tmp_path}test.snirf", verbose=True)
    out = capsys.readouterr().out
    assert result is None and "Valid SNIRFFile" not in out
    assert "One of measurementList or measurementLists" in out


def test_mismatched_datatimeseries_measurementlist(tmp_path, capsys):
    result = read_snirf(VALID_SNIRF_ML_PATH)
    result.nirs[0].data[0].measurementList = result.nirs[0].data[0].measurementList[:-1]
    result.save(f"{tmp_path}test.snirf")
    result = read_snirf(f"{tmp_path}test.snirf", verbose=True)
    out = capsys.readouterr().out
    assert result is None and "Valid SNIRFFile" not in out
    assert "Field dataTimeSeries and measurementList should match" in out


def test_mismatched_datatimeseries_measurementlists(tmp_path, capsys):
    result = read_snirf(VALID_SNIRF_MLS_PATH)
    result.nirs[0].data[0].dataTimeSeries = result.nirs[0].data[0].dataTimeSeries[:, :-1]
    result.save(f"{tmp_path}test.snirf")
    result = read_snirf(f"{tmp_path}test.snirf", verbose=True)
    out = capsys.readouterr().out
    assert result is None and "Valid SNIRFFile" not in out
    assert "Field dataTimeSeries and measurementLists should match" in out


def test_mismatched_datatimeseries_dataoffset(tmp_path, capsys):
    result = read_snirf(VALID_SNIRF_ML_PATH)
    shape_datatimeseries = result.nirs[0].data[0].dataTimeSeries.shape
    result.nirs[0].data[0].dataOffset = np.zeros(shape_datatimeseries[1] - 1)
    result.save(f"{tmp_path}test.snirf")
    result = read_snirf(f"{tmp_path}test.snirf", verbose=True)
    out = capsys.readouterr().out
    assert result is None and "Valid SNIRFFile" not in out
    assert "Field dataTimeSeries and dataOffset should match" in out


def test_mismatched_datatimeseries_time(tmp_path, capsys):
    result = read_snirf(VALID_SNIRF_ML_PATH)
    result.nirs[0].data[0].time = result.nirs[0].data[0].time[:-1]
    result.save(f"{tmp_path}test.snirf")
    result = read_snirf(f"{tmp_path}test.snirf", verbose=True)
    out = capsys.readouterr().out
    assert result is None and "Valid SNIRFFile" not in out
    assert "Field dataTimeSeries and time should match" in out


def test_invalid_data(tmp_path, capsys):
    result = read_snirf(VALID_SNIRF_ML_PATH)
    result.nirs[0].stim[0].data = result.nirs[0].stim[0].data[:, :2]
    result.save(f"{tmp_path}test.snirf")
    result = read_snirf(f"{tmp_path}test.snirf", verbose=True)
    out = capsys.readouterr().out
    assert result is None and "Valid SNIRFFile" not in out
    assert "Field data should have at least 3 columns" in out


def test_valid_datalabels(tmp_path, capsys):
    result = read_snirf(VALID_SNIRF_ML_PATH)
    result.nirs[0].stim[0].dataLabels = np.array(
        [b'label']*result.nirs[0].stim[0].data.shape[1],
        dtype=object
    )
    result.save(f"{tmp_path}test.snirf")
    result = read_snirf(f"{tmp_path}test.snirf", verbose=True)
    out = capsys.readouterr().out
    assert result is not None and "Valid SNIRFFile" in out
    assert "error" not in out.lower()
    assert "warning" not in out.lower()


def test_mismatched_datalabels_data(tmp_path, capsys):
    result = read_snirf(VALID_SNIRF_ML_PATH)
    result.nirs[0].stim[0].dataLabels = np.array(
        [b'label']*(result.nirs[0].stim[0].data.shape[1]-1),
        dtype=object
    )
    result.save(f"{tmp_path}test.snirf")
    result = read_snirf(f"{tmp_path}test.snirf", verbose=True)
    out = capsys.readouterr().out
    assert result is None and "Valid SNIRFFile" not in out
    assert "Field dataLabels and data should match" in out


def test_missing_source_positions(tmp_path, capsys):
    result = read_snirf(VALID_SNIRF_ML_PATH)
    del result.nirs[0].probe.sourcePos2D
    result.save(f"{tmp_path}test.snirf")
    result = read_snirf(f"{tmp_path}test.snirf", verbose=True)
    out = capsys.readouterr().out
    assert result is None and "Valid SNIRFFile" not in out
    assert "At least one of sourcePos2D or sourcePos3D is required" in out


def test_missing_detector_positions(tmp_path, capsys):
    result = read_snirf(VALID_SNIRF_ML_PATH)
    del result.nirs[0].probe.detectorPos2D
    result.save(f"{tmp_path}test.snirf")
    result = read_snirf(f"{tmp_path}test.snirf", verbose=True)
    out = capsys.readouterr().out
    assert result is None and "Valid SNIRFFile" not in out
    assert "At least one of detectorPos2D or detectorPos3D is required" in out


def test_valid_coordinatesystem(tmp_path, capsys):
    result = read_snirf(VALID_SNIRF_ML_PATH)
    result.nirs[0].probe.coordinateSystem = RECOGNIZED_COORDINATE_SYSTEMS[0]
    result.save(f"{tmp_path}test.snirf")
    result = read_snirf(f"{tmp_path}test.snirf", verbose=True)
    out = capsys.readouterr().out
    assert result is not None and "Valid SNIRFFile" in out
    assert "error" not in out.lower()
    assert "warning" not in out.lower()


def test_warn_unrecognized_coordinatesystem(tmp_path, capsys):
    result = read_snirf(VALID_SNIRF_ML_PATH)
    result.nirs[0].probe.coordinateSystem = 'unrecognized'
    result.nirs[0].probe.coordinateSystemDescription = 'unrecognized'
    result.save(f"{tmp_path}test.snirf")
    result = read_snirf(f"{tmp_path}test.snirf", verbose=True)
    out = capsys.readouterr().out
    assert result is not None and "Valid SNIRFFile" in out
    assert "warning" in out.lower()
    assert "Value of coordinateSystem is not recognized" in out
    assert "Field coordinateSystemDescription is required" not in out


def test_warn_missing_coordinatesystemdescription(tmp_path, capsys):
    result = read_snirf(VALID_SNIRF_ML_PATH)
    result.nirs[0].probe.coordinateSystem = 'unrecognized'
    result.save(f"{tmp_path}test.snirf")
    result = read_snirf(f"{tmp_path}test.snirf", verbose=True)
    out = capsys.readouterr().out
    assert result is not None and "Valid SNIRFFile" in out
    assert "warning" in out.lower()
    assert "Value of coordinateSystem is not recognized" in out
    assert "Field coordinateSystemDescription is required" in out


# LEVEL -3 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def test_warn_zero_ml_index(tmp_path, capsys):
    result = read_snirf(VALID_SNIRF_ML_PATH)
    result.nirs[0].data[0].measurementList[0].sourceIndex = 0
    result.save(f"{tmp_path}test.snirf")
    result = read_snirf(f"{tmp_path}test.snirf", verbose=True)
    out = capsys.readouterr().out
    assert result is not None and "Valid SNIRFFile" in out
    assert "warning" in out.lower()
    assert "An index of zero in sourceIndex is usually undefined" in out


def test_invalid_ml_index(tmp_path, capsys):
    result = read_snirf(VALID_SNIRF_ML_PATH)
    result.nirs[0].data[0].measurementList[0].sourceIndex = -1
    result.save(f"{tmp_path}test.snirf")
    result = read_snirf(f"{tmp_path}test.snirf", verbose=True)
    out = capsys.readouterr().out
    assert result is None and "Valid SNIRFFile" not in out
    assert "Input should be a valid integer greater than or equal to 0" in out


def test_valid_ml_datatypelabel(tmp_path, capsys):
    result = read_snirf(VALID_SNIRF_ML_PATH)
    result.nirs[0].data[0].measurementList[0].dataTypeLabel = RECOGNIZED_DATA_TYPE_LABELS[0]
    result.save(f"{tmp_path}test.snirf")
    result = read_snirf(f"{tmp_path}test.snirf", verbose=True)
    out = capsys.readouterr().out
    assert result is not None and "Valid SNIRFFile" in out
    assert "error" not in out.lower()
    assert "warning" not in out.lower()


def test_warn_unrecognized_ml_datatypelabel(tmp_path, capsys):
    result = read_snirf(VALID_SNIRF_ML_PATH)
    result.nirs[0].data[0].measurementList[0].dataTypeLabel = 'unrecognized'
    result.save(f"{tmp_path}test.snirf")
    result = read_snirf(f"{tmp_path}test.snirf", verbose=True)
    out = capsys.readouterr().out
    assert result is not None and "Valid SNIRFFile" in out
    assert "warning" in out.lower()
    assert "Value of dataTypeLabel is not recognized" in out


def test_warn_unrecognized_ml_datatype(tmp_path, capsys):
    result = read_snirf(VALID_SNIRF_ML_PATH)
    result.nirs[0].data[0].measurementList[0].dataType = 42
    result.save(f"{tmp_path}test.snirf")
    result = read_snirf(f"{tmp_path}test.snirf", verbose=True)
    out = capsys.readouterr().out
    assert result is not None and "Valid SNIRFFile" in out
    assert "warning" in out.lower()
    assert "Value of dataType is not recognized" in out


def test_missing_ml_datatype(tmp_path, capsys):
    result = read_snirf(VALID_SNIRF_ML_PATH)
    result.nirs[0].data[0].measurementList[0].dataType = 99999
    result.save(f"{tmp_path}test.snirf")
    result = read_snirf(f"{tmp_path}test.snirf", verbose=True)
    out = capsys.readouterr().out
    assert result is None and "Valid SNIRFFile" not in out
    assert "Field dataTypeLabel is required when dataType is 99999" in out
