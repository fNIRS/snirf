import os
import urllib.request

from snirf_validator import validate_snirf


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
snirf = validate_snirf(filename)
