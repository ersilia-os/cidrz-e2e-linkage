import os
import zipfile
import tempfile
import shutil
import json
import gdown

from .. import logger
from ..vars import MODELS_PATH


FILE_ID = {
    "linkage.zip": "1mvBm_nJ2v-RuwQ78k7ZRhO8SurADONGn",
    "schema.zip": "1YTlUvaJm8C09m0Krc13zBe5okiQ7GOul",
    "name_ngram.pkl.zip": "1mx755FJQQmyTFBdFDGGqoJaORl-Tptag",
}


class GoogleDriveDownloader(object):
    def __init__(self):
        pass

    def download_file_from_google_drive(self, file_id, destination):
        url = "https://drive.google.com/uc?id={0}".format(file_id)
        output = "here.zip"
        gdown.download(url, destination, quiet=False)

    def fetch_zip(self, file_id, destination):
        """Download file from google docs. The file id is necessary. A .zip file is assumed."""
        tmp_zip = tempfile.NamedTemporaryFile(dir=destination).name + ".zip"
        tmp_zip = file_id + ".zip"
        self.download_file_from_google_drive(file_id, tmp_zip)
        with zipfile.ZipFile(tmp_zip, "r") as zip_ref:
            zip_ref.extractall(destination)
        os.remove(tmp_zip)


class Downloader(object):
    def __init__(self):
        self.models_path = os.path.abspath(MODELS_PATH)
        self.downloader = GoogleDriveDownloader()

    def _status_file_name(self):
        return os.path.join(MODELS_PATH, "download_status.json")

    def is_done(self):
        status_file = self._status_file_name()
        if not os.path.exists(status_file):
            return False
        with open(status_file, "r") as f:
            status = json.load(f)
        if status["status"]:
            return True
        else:
            return False

    def download(self):
        logger.info("Downloading data and models for standard mode")
        for f in ["linkage.zip", "schema.zip", "name_ngram.pkl.zip"]:
            logger.debug("Downloading file {0}".format(f))
            file_id = FILE_ID[f]
            self.downloader.fetch_zip(file_id, self.models_path)
        macosx_folder = os.path.join(MODELS_PATH, "__MACOSX")
        if os.path.exists(macosx_folder):
            shutil.rmtree(macosx_folder)
        status_file = self._status_file_name()
        logger.debug("Saving status file {0}".format(status_file))
        status = {"status": True}
        with open(status_file, "w") as f:
            json.dump(status, f, indent=True)

    def download_dev(self):
        logger.info("Downloading data and models for developer mode")
        pass  # TODO
