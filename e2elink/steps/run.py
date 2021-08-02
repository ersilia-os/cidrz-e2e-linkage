from .. import logger

from .setup.setup import PipelineSetup
from .schema.schema import SchemaMatcher
from .preprocess.preprocess import Preprocessor
from .block.block import Blocker
from .compare.compare import Compare
from .score.score import Scorer
from .evaluate.evaluate import Evaluator
from .finish.finish import Finisher


BLOCKING_K = 5


class RunAll(object):
    def __init__(self, src_file, trg_file, truth_file=None, output_dir=None):
        self.src_file = src_file
        self.trg_file = trg_file
        self.truth_file = truth_file
        self.output_dir = output_dir

    def run(self):
        logger.debug("Setup")
        ps = PipelineSetup(
            self.src_file, self.trg_file, self.truth_file, self.output_dir
        )
        ps.setup()
        logger.debug("Schema")
        sm = SchemaMatcher().match()
        sm.save()
        logger.debug("Preprocess")
        prep = Preprocessor().clean()
        prep.save()
        logger.debug("Block")
        bl = Blocker().block(BLOCKING_K)
        bl.save()
        logger.debug("Compare")
        comp = Compare().compare()
        comp.save()
        logger.debug("Score")
        sc = Scorer().score()
        sc.save()
        logger.debug("Evaluate")
        eval = Evaluator().evaluate()
        eval.save()
        logger.debug("Finish")
        fin = Finisher().finish()
        fin.save()
        logger.success("Record linkage pipeline successful!")
