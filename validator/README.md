# SNIRF Blueprint

## Install the package

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
