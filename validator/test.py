import os
import urllib.request

from snirf_schema import read_snirf


# =============================================================================
# DOWNLOAD FILE
# =============================================================================
filename = "neuro_run01.snirf"
url = (
    "https://github.com/fNIRS/snirf-samples/raw/master/"
    f"basic/{filename}"
)

if not os.path.exists(filename):
    urllib.request.urlretrieve(url, filename)


# =============================================================================
# VALIDATE FILE
# =============================================================================
snirf = read_snirf(filename, warnings=True)


# =============================================================================
# WRITE
# =============================================================================
snirf.save('new_'+filename)
