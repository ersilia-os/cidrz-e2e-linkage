import os
import zipfile
import requests
import tempfile

from .. import logger
from ..vars import MODELS_PATH


FILE_ID = {
    "linkage.zip": "1mvBm_nJ2v-RuwQ78k7ZRhO8SurADONGn",
    "schema.zip": "1n3JDjTdh6hAMK-dVKF1AFa9WS5a5inoM",
    "name_ngram.pkl.zip": "1mx755FJQQmyTFBdFDGGqoJaORl-Tptag",
}


class GoogleDriveDownloader(object):
    def __init__(self):
        pass

    @staticmethod
    def get_confirm_token(response):
        for key, value in response.cookies.items():
            if key.startswith("download_warning"):
                return value
        return None

    @staticmethod
    def save_response_content(response, destination):
        chunk_size = 32768
        with open(destination, "wb") as f:
            for chunk in response.iter_content(chunk_size):
                if chunk:
                    f.write(chunk)

    def download_file_from_google_drive(self, file_id, destination):
        url = "https://docs.google.com/uc?export=download"
        session = requests.Session()
        response = session.get(url, params={"id": file_id}, stream=True)
        token = self.get_confirm_token(response)
        if token:
            params = {"id": id, "confirm": token}
            response = session.get(url, params=params, stream=True)
        self.save_response_content(response, destination)

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
        logger.debug(
            "Downloader initialized. Files will be stored at {0}".format(
                self.models_path
            )
        )
        self.downloader = GoogleDriveDownloader()

    def download(self):
        logger.info("Downloading data in standard mode")
        for f in ["linkage.zip", "schema.zip", "name_ngram.pkl.zip"]:
            logger.debug("Downloading file {0}".format(f))
            file_id = FILE_ID[f]
            self.downloader.fetch_zip(file_id, self.models_path)

    def download_dev(self):
        logger.info("Downloading for developer mode")
        pass
