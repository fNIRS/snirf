# SNIRF Blueprint Validator


## Install

1. [Install Python 3.12 or newer](https://www.anaconda.com/download/success?reg=skipped)


2. Create an environment:
```bash
conda create -n snirfblueprint
conda activate snirfblueprint
```

3. Install the package with its dependencies:
```bash
pip install .
```


## Usage

In a terminal:
```bash
snirfblueprint <my_snirf_file_to_validate.snirf>
```

Or in a Python script:
```python
from snirfblueprint import read_snirf

# Read SNIRF file
filename = "path/to/original/valid_ml.snirf"
snirf = read_snirf(filename, verbose=True)

# It is possible to edit the SNIRF object
snirf.nirs[0].metaDataTags.SubjectID = 'P1'

# Save as SNIRF file
snirf.save('path/to/new/valid_ml.snirf')
```


## Development

All the SNIRF specifications are implemented as a Pydantic schema in `snirfblueprint.py`. The package contains a SNIRF reader (SNIRF to Pydantic model) as well as a SNIRF writer (Pydantic model to SNIRF).

**Install in editable mode with development requirements:**
```bash
pip install -e .[dev]
```

**Run the test suite:**
```bash
pytest snirfblueprint/tests -v
```
