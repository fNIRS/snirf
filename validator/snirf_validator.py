import h5py

from snirf_reader import validate_snirf


# =============================================================================
# CHECK FILE
# =============================================================================
def print_hdf5_tree(group, indent=0):
    for key, item in group.items():
        print(" " * indent + key, type(item).__name__)
        if isinstance(item, h5py.Group):
            print_hdf5_tree(item, indent + 2)


f = h5py.File("neuro_run01.snirf", "r")
# print_hdf5_tree(f)


# =============================================================================
# VALIDATE FILE
# =============================================================================
snirf = validate_snirf(
    "neuro_run01.snirf"
)
