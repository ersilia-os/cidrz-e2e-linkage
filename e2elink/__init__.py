# Version
from ._version import __version__

del _version

# External imports
import os

# Check necessary data and models
HOME = ".e2elink"
if not os.path.exists(HOME):
    os.mkdir(HOME)

# Data path. Download if not exists
DATA_PATH = os.path.join(HOME, "data")
DATA_PATH = "/Users/mduran/github/cidrz/cidrz-e2e-linkage/data"
if not os.path.exists(DATA_PATH):
    pass  # TODO download

# Models path. Download if not exists
MODELS_PATH = os.path.join(HOME, "models")
MODELS_PATH = "/Users/mduran/github/cidrz/cidrz-e2e-linkage/models"
if not os.path.exists(MODELS_PATH):
    pass  # TODO download


__all__ = ["__version__"]
