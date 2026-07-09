import re
import h5py
import numpy as np


# =============================================================================
# HDF5 LOADERS
# =============================================================================
def read_dataset(hdf5_dataset):
    """
    Convert HDF5 dataset into a Python object or numpy array.
    """

    value = hdf5_dataset[()]

    # Unwrap scalar-like arrays
    if isinstance(value, np.ndarray) and value.size == 1:
        value = value.reshape(()).item()

    # Decode scalar bytes
    if isinstance(value, (bytes, np.bytes_)):
        return value.decode()

    # Convert numpy scalar
    if isinstance(value, np.generic):
        return value.item()

    # Decode arrays of bytes
    if isinstance(value, np.ndarray) and value.dtype == object:
        if all(isinstance(x, (bytes, np.bytes_)) for x in value.flat):
            value = np.vectorize(lambda x: x.decode())(value)

    return value


def read_simple_group(group):
    """
    Convert a simple HDF5 group into a dictionary.
    """

    result = {}

    for name, item in group.items():

        if isinstance(item, h5py.Dataset):
            result[name] = read_dataset(item)

        elif isinstance(item, h5py.Group):
            result[name] = read_simple_group(item)

    return result


def find_indexed_groups(group, prefix):
    """
    Find indexed groups and return them sorted numerically.
    """

    indexed = []

    pattern = re.compile(prefix + r"(\d+)")

    for name, item in group.items():
        if isinstance(item, h5py.Group):
            match = pattern.fullmatch(name)
            if match:
                indexed.append((int(match.group(1)), item))

    indexed.sort(key=lambda x: x[0])

    return [item for _, item in indexed]


def read_indexed_groups(group, prefix):
    """
    Convert indexed groups into a list of dictionaries.
    """

    return [read_simple_group(item)
            for item in find_indexed_groups(group, prefix)]


def has_indexed_groups(group, prefix):
    """
    Check whether indexed groups exist.
    """

    pattern = re.compile(prefix + r"\d+")

    return any(isinstance(item, h5py.Group) and pattern.fullmatch(name)
               for name, item in group.items())


def read_single_or_indexed_groups(group, prefix, loader):
    """
    Handle simple or indexed groups ([prefix] vs. [prefix1, prefix2]).
    """
    has_single = prefix in group
    has_indexed = has_indexed_groups(group, prefix)

    if has_single and has_indexed:
        raise ValueError(f"Cannot have both '{prefix}' and '{prefix}{{i}}'")

    if has_single:
        return [loader(group[prefix])]

    return [loader(item) for item in find_indexed_groups(group, prefix)]


# =============================================================================
# SNIRF LOADERS
# =============================================================================
def read_data(data_group):
    data = read_simple_group(data_group)

    has_measurement_list = has_indexed_groups(data_group, "measurementList")
    has_measurement_lists = ("measurementLists" in data_group)

    if has_measurement_list:
        data.pop("measurementList", None)
        data["measurementList"] = (
            read_indexed_groups(data_group, "measurementList")
        )

    if has_measurement_lists:
        data.pop("measurementLists", None)
        data["measurementLists"] = (
            read_simple_group(data_group["measurementLists"])
        )

    return data


def load_nirs(nirs_group):
    result = {}

    # Metadata
    result["metaDataTags"] = read_simple_group(nirs_group["metaDataTags"])

    # Data
    result["data"] = read_single_or_indexed_groups(
        nirs_group, "data", read_data
    )

    # Stim
    result["stim"] = read_single_or_indexed_groups(
        nirs_group, "stim", read_simple_group
    )

    # Probe
    result["probe"] = read_simple_group(nirs_group["probe"])

    # Aux
    result["aux"] = read_single_or_indexed_groups(
        nirs_group, "aux", read_simple_group
    )

    return result


def load_snirf(filename, SNIRFFile):
    """
    Main entry point.
    """
    with h5py.File(filename, "r") as f:
        data = {
            "formatVersion": read_dataset(f["formatVersion"]),
            "nirs": read_single_or_indexed_groups(f, "nirs", load_nirs)
        }
    return SNIRFFile(**data)
