import os
import shutil
from .. import logger


ROOT = os.path.dirname(os.path.abspath(__file__))

class Example(object):

    def __init__(self):
        self.dir = os.getcwd()

    def _copy(self, filename):
        shutil.copyfile(os.path.join(ROOT, "files", filename), os.path.join(self.dir, filename))

    def get(self):
        self._copy("source.csv")
        self._copy("target.csv")
        self._copy("truth.csv")
        logger.debug("Example files stored in {0}".format(self.dir))
