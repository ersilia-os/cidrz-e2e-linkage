from .. import logger

from .setup.setup import PipelineSetup
from .schema.schema import SchemaMatcher
from .preprocess.preprocess import Preprocessor
from .block.block import Blocker
from .preprocessing.e2e_pprocessor import PreprocessPipelineHandler
from .compare.compare import Compare
from .score.score import Scorer
from .evaluate.evaluate import Evaluator
from .finish.finish import Finisher


BLOCKING_K = 5


class RunAll(object):
    def __init__(self, src_file, trg_file, truth_file=None, output_dir=None, column_mapping_file=None):
        self.src_file = src_file
        self.trg_file = trg_file
        self.truth_file = truth_file
        self.output_dir = output_dir
        self.column_mapping_file = column_mapping_file

    def run(self):
        logger.debug("Setup")
        ps = PipelineSetup(
            self.src_file, self.trg_file, self.truth_file, self.output_dir, self.column_mapping_file
        )
        ps.setup()

        if ps.column_mapping is None:
            logger.debug("Schema")
            sm = SchemaMatcher().match()
            sm.save()

            ps.column_mapping = sm.load()

        logger.debug("Preprocess")
        #prep = Preprocessor().clean()
        #prep.save()
        prep = PreprocessPipelineHandler(ps, ps.column_mapping)
        prep.clean()
        src, src_columns, trg, trg_columns = prep.save()

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
