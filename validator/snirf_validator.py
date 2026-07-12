import h5py
import os
import re

from pydantic_core import ValidationError
from snirf_schema import SNIRFFile, RECOGNIZED_INDEXED_PREFIXES

GREEN = '\033[32m'
ORANGE = '\033[33m'
RED = '\033[31m'
RESET = '\033[0m'


class ValidationReport:
    def __init__(self):
        self.warnings: list[str] = []

    def add_warning(self, message: str):
        self.warnings.append(message)

    def print_warnings(self):
        if self.warnings:
            print(
                f"{ORANGE}{len(self.warnings)} validation warnings for",
                f"SNIRFFile{RESET}"
            )
            for warning in self.warnings:
                print(f"{ORANGE}  {warning}{RESET}")


# =============================================================================
# SNIRF GROUP LOADER
# =============================================================================
def load_snirf_group(group, group_name):
    result = {}

    for name, item in group.items():
        if isinstance(item, h5py.Dataset):
            result[name] = item[()]
        elif isinstance(item, h5py.Group):
            result[name] = load_snirf_group(item, name)

    # Sort by keys
    result = dict(sorted(result.items()))

    # Group indexed groups with valid prefixes
    if "stim" not in group_name:  # avoid grouping stim.data
        for valid_indexed_prefix in RECOGNIZED_INDEXED_PREFIXES:
            pattern = rf"^{re.escape(valid_indexed_prefix)}(\d+)?$"
            indexed_keys = [k for k in result.keys() if re.match(pattern, k)]
            if indexed_keys:
                indexed_items = [result[key] for key in indexed_keys]
                # Remove items with indexed names
                for key in indexed_keys:
                    del result[key]
                # Add new item with a list of indexed groups
                result[valid_indexed_prefix] = indexed_items

    return result


# =============================================================================
# SNIRF VALIDATOR
# =============================================================================
def validate_snirf(filename):
    print("===============")
    print("SNIRF VALIDATOR")
    print("---------------")
    snirf = None

    if not filename.endswith('.snirf'):
        print(f"{RED}ERROR: Valid SNIRF files must end with .snirf{RESET}")

    else:
        report = ValidationReport()
        with h5py.File(filename, "r") as f:
            data = load_snirf_group(f, os.path.basename(filename))
        try:
            snirf = SNIRFFile.model_validate(data, context={"report": report})
            print(f"{GREEN}Valid SNIRFFile{RESET}")
        except ValidationError as e:
            print(f"{RED}{e}{RESET}")
        finally:
            report.print_warnings()

    return snirf
