# Remove warnings (especially for sklearn)
def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

# Version
from ._version import __version__

del _version

# External imports
import os

# Internal imports
from .utils.logging import logger

# Path variables
from .vars import MODELS_PATH
from .vars import E2ELINK_DIR

# Download data if not done
from .utils.download import Downloader
dw = Downloader()
if not dw.is_done():
    logger.info("Downloading necessary data and models, as they are not available in {0}".format(MODELS_PATH))
    dw.download()


__all__ = ["__version__"]
