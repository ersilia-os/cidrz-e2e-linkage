# Version
from ._version import __version__

del _version

# External imports
import os

# Internal imports
from .utils.logging import logger

# Path variables
from .vars import MODELS_PATH


__all__ = ["__version__"]
