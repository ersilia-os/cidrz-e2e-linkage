import sys
import os
import shutil

from e2elink import MODELS_PATH
from e2elink import logger
from e2elink.steps.setup.setup import PipelineSetup
from e2elink.steps.schema.schema import SchemaMatcher
from e2elink.steps.preprocess.preprocess import Preprocessor
from e2elink.steps.block.block import Blocker
from e2elink.steps.compare.compare import Compare
from e2elink.steps.score.score import Scorer


k = 5


class Trainer(object):
    def __init__(self, tag):
        self.tag = tag
        self.input_dir = os.path.join(MODELS_PATH, "linkage", "data", "raw", tag)
        logger.debug("Setting up trainer for directory {0}".format(self.input_dir))
        self.output_dir = os.path.join(MODELS_PATH, "linkage", "results", tag)
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)
        logger.debug("Results will be stored at {0}".format(self.output_dir))
        self.src_file = os.path.join(self.input_dir, "source.csv")
        self.trg_file = os.path.join(self.input_dir, "target.csv")
        self.truth_file = os.path.join(self.input_dir, "truth.csv")

    def _setup(self):
        ps = PipelineSetup(
            self.src_file, self.trg_file, self.truth_file, self.output_dir
        )
        ps.setup()
        logger.debug("Setup done")

    def _schema(self):
        schema = SchemaMatcher().match()
        schema.save()
        logger.debug("Schema done")

    def _preprocess(self):
        prep = Preprocessor().clean()
        prep.save()
        logger.debug("Preprocess done")

    def _block(self):
        bl = Blocker().block(k)
        bl.save()
        logger.debug("Blocking done")

    def _compare(self):
        comp = Compare().compare()
        comp.save()
        logger.debug("Compare done")

    def _score(self):
        sc = Scorer().score()
        sc.save()
        logger.debug("Scorer done")

    def prepare(self):
        logger.info("Preparing")
        self._setup()
        self._schema()
        self._preprocess()
        self._block()
        self._compare()

    def train(self):
        logger.info("Preparing")
        self.prepare()
        logger.info("Training")
        self._score()


if __name__ == "__main__":
    tag = "0fafb9bd-262a-4d92-a7e4-aac3a3fa7605"
    tr = Trainer(tag)
    tr.train()
