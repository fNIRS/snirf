import numpy as np
from snirf_schema import read_snirf, MeasurementLists

VALID_SNIRF_PATH = "simple_probe_valid.snirf"


def test_valid_no_warnings(capsys):
    result = read_snirf(VALID_SNIRF_PATH, verbose=True)
    out = capsys.readouterr().out
    assert result is not None and "Valid SNIRFFile" in out
    assert "error" not in out.lower()
    assert "warning" not in out.lower()


def test_invalid_extension(tmp_path, capsys):
    result = read_snirf(VALID_SNIRF_PATH)
    result.save(f"{tmp_path}test.nirs")
    result = read_snirf(f"{tmp_path}test.nirs", verbose=True)
    out = capsys.readouterr().out
    assert result is None and "Valid SNIRFFile" not in out
    assert "ERROR: Valid SNIRF files must end with .snirf" in out


def test_missing_nirs(tmp_path, capsys):
    result = read_snirf(VALID_SNIRF_PATH)
    del result.nirs
    result.save(f"{tmp_path}test.snirf")
    result = read_snirf(f"{tmp_path}test.snirf", verbose=True)
    out = capsys.readouterr().out
    assert result is None and "Valid SNIRFFile" not in out
    assert "\nnirs\n  Field required" in out


def test_measurementlist_measurementlists(tmp_path, capsys):
    result = read_snirf(VALID_SNIRF_PATH)
    mls = {
        'sourceIndex': np.empty((0, 1), dtype=int),
        'detectorIndex': np.empty((0, 1), dtype=int),
        'wavelengthIndex': np.empty((0, 1), dtype=int),
        'dataType': np.empty((0, 1), dtype=int),
        'dataTypeIndex': np.empty((0, 1), dtype=int),
        'sourcePower': np.empty((0, 1), dtype=float),
        'detectorGain': np.empty((0, 1), dtype=float),
    }
    for ml in result.nirs[0].data[0].measurementList:
        for key, value in ml.model_dump(exclude_unset=True).items():
            mls[key] = np.append(mls[key], value)
    result.nirs[0].data[0].measurementLists = MeasurementLists(**mls)
    result.save(f"{tmp_path}test.snirf")
    result = read_snirf(f"{tmp_path}test.snirf", verbose=True)
    out = capsys.readouterr().out
    assert result is None and "Valid SNIRFFile" not in out
    assert "measurementList and measurementLists cannot both be present" in out


def test_no_measurementlist_no_measurementlists(tmp_path, capsys):
    result = read_snirf(VALID_SNIRF_PATH)
    del result.nirs[0].data[0].measurementList
    result.save(f"{tmp_path}test.snirf")
    result = read_snirf(f"{tmp_path}test.snirf", verbose=True)
    out = capsys.readouterr().out
    assert result is None and "Valid SNIRFFile" not in out
    assert "Strictly one of measurementList or measurementLists" in out


def test_valid_measurementlists(tmp_path, capsys):
    result = read_snirf(VALID_SNIRF_PATH)
    mls = {
        'sourceIndex': np.empty((0, 1), dtype=int),
        'detectorIndex': np.empty((0, 1), dtype=int),
        'wavelengthIndex': np.empty((0, 1), dtype=int),
        'dataType': np.empty((0, 1), dtype=int),
        'dataTypeIndex': np.empty((0, 1), dtype=int),
        'sourcePower': np.empty((0, 1), dtype=float),
        'detectorGain': np.empty((0, 1), dtype=float),
    }
    for ml in result.nirs[0].data[0].measurementList:
        for key, value in ml.model_dump(exclude_unset=True).items():
            mls[key] = np.append(mls[key], value)
    result.nirs[0].data[0].measurementLists = MeasurementLists(**mls)
    del result.nirs[0].data[0].measurementList
    result.save(f"{tmp_path}test.snirf")
    result = read_snirf(f"{tmp_path}test.snirf", verbose=True)
    out = capsys.readouterr().out
    assert result is not None and "Valid SNIRFFile" in out
    assert "error" not in out.lower()
    assert "warning" not in out.lower()
