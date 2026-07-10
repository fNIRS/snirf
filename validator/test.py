import h5py
import os
import urllib.request

from snirf_validator import validate_snirf


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================
def print_hdf5_tree(group, indent=0):
    for key, item in group.items():
        print(" " * indent + key, type(item).__name__)
        if isinstance(item, h5py.Group):
            print_hdf5_tree(item, indent + 2)


# =============================================================================
# INSPECT
# =============================================================================
filename = "neuro_run01.snirf"
url = (
    "https://github.com/fNIRS/snirf-samples/raw/master/"
    f"basic/{filename}"
)

if not os.path.exists(filename):
    urllib.request.urlretrieve(url, filename)

f = h5py.File(filename, "r")
print("==============")
print("HDF5 structure")
print("--------------")
print_hdf5_tree(f)


# =============================================================================
# VALIDATE FILE
# =============================================================================
snirf = validate_snirf(
    filename
)