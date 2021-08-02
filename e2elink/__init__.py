# Version
from ._version import __version__

del _version

# External imports
import os

# Internal imports
from .utils.logging import logger

# Path variables
from .vars import E2ELINK_DIR
from .vars import MODELS_PATH
from .vars import DATA_PATH

# Download data if not done
from .utils.download import Downloader

dw = Downloader()
if not dw.is_done():
    logger.info(
        "Downloading necessary data and models, as they are not available in {0}".format(
            MODELS_PATH
        )
    )
    dw.download()

# Remove warnings (especially for sklearn)
import warnings


def warn(*args, **kwargs):
    pass


warnings.warn = warn


__all__ = ["__version__"]
