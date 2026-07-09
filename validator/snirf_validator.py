import h5py

from snirf_schema import SNIRFFile
from snirf_reader import load_snirf


# =============================================================================
# CHECK FILE
# =============================================================================
def print_hdf5_tree(group, indent=0):
    for key, item in group.items():
        print(" " * indent + key, type(item).__name__)
        if isinstance(item, h5py.Group):
            print_hdf5_tree(item, indent + 2)


f = h5py.File("Simple_Probe.snirf", "r")
print_hdf5_tree(f)


# =============================================================================
# VALIDATE FILE
# =============================================================================
snirf = load_snirf(
    "Simple_Probe.snirf",
    SNIRFFile
)
