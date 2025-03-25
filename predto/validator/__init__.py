# Versioning system for the package.
__version__ = "1.1.4"
version_split = __version__.split(".")
__spec_version__ = (
    (1000 * int(version_split[0]))  # Major version * 1000
    + (10 * int(version_split[1]))  # Minor version * 10
    + (1 * int(version_split[2]))   # Patch version * 1
)

import importlib

# Import miner dynamically to avoid circular import issues
miner = importlib.import_module("predto.miner")

# This allows easy access to the versioning info within the package.
def get_version():
    """Returns the version of the package as a string."""
    return __version__

def get_spec_version():
    """Returns the spec version as an integer."""
    return __spec_version__

# Import validator dynamically to avoid self-referential circular import
validator = importlib.import_module("predto.validator")
