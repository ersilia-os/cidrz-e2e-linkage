import os
from .. import logger
from ..vars import E2ELINK_DIR


class Downloader(object):

    def __init__(self):
        self.dest_dir = os.path.abspath(E2ELINK_DIR)
        logger.debug("Downloader initialized. Files will be stored at {0}".format(self.dest_dir))

    def download_for_inference(self):
        logger.info("Downloading data for inference mode")
        pass

    def download_for_synthetic(self):
        logger.info("Downloading data for synthetic mode")
        pass

    def download_for_training(self):
        logger.info("Downloading data for training mode")
        pass
