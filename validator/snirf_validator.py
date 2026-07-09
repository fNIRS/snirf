import h5py

from snirf_schema import SNIRFFile
from snirf_reader import load_snirf


# =============================================================================
# HDF5 TREE
# =============================================================================
def print_hdf5_tree(group, indent=0):
    for key, item in group.items():
        print(" " * indent + key, type(item).__name__)
        if isinstance(item, h5py.Group):
            print_hdf5_tree(item, indent + 2)


with h5py.File("sub-01_task-tapping_nirs.snirf", "r") as f:
    print_hdf5_tree(f)


# =============================================================================
# VALIDATE
# =============================================================================
snirf = load_snirf(
    "sub-01_task-tapping_nirs.snirf",
    SNIRFFile
)
