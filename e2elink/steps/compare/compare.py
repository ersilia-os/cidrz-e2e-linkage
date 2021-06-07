import os
import json
import numpy as np

from .columns import CompareGetter
from ... import logger
from ..setup.setup import Session
from ..preprocess.preprocess import Preprocess
from ..block.block import Block


class Comparison(object):
    def __init__(self, C=None, columns=None):
        self.C = C
        self.columns = columns
        self.path = os.path.join(Session().get_output_path(), "compare")
        self.C_path = os.path.join(self.path, "C.npy")
        self.columns_path = os.path.join(self.path, "columns.json")

    def save(self):
        with open(self.C_path, "wb") as f:
            np.save(f, self.C, allow_pickle=False)
        logger.debug("Comparisons saved to {0}".format(self.C_path))
        with open(self.columns_path, "w") as f:
            json.dump(self.columns, f, indent=4)
        logger.debug("Columns saved to {0}".format(self.columns_path))

    def load(self):
        logger.debug("Loading comparisons from {0}".format(self.C_path))
        with open(self.C_path, "rb") as f:
            C = np.load(f)
        logger.debug("Loading columns from {0}".format(self.columns_path))
        with open(self.columns_path, "r") as f:
            columns = json.load(f)
        return Comparison(C, columns)


class _Compare(object):
    def __init__(self):
        self._compare_getter = CompareGetter()

    @staticmethod
    def _get_compare_columns(src, trg):
        src_cols = list(src.columns)
        trg_cols = set(list(trg.columns))
        return [col for col in src_cols if col in trg_cols]

    @staticmethod
    def _read_column_data_src_trg(pairs, src, trg, col):
        # source data
        col_src = list(src[col])
        idx_src = list(pairs["src"])
        data_src = [col_src[i] for i in idx_src]
        # target data
        col_trg = list(trg[col])
        idx_trg = list(pairs["trg"])
        data_trg = [col_trg[i] for i in idx_trg]
        return data_src, data_trg

    def compare(self, pairs, src, trg):
        cols = self._get_compare_columns(src, trg)
        C = []
        columns = []
        for col in cols:
            logger.debug("Comparing column {0}".format(col))
            comp = self._compare_getter.get(col)
            data_src, data_trg = self._read_column_data_src_trg(pairs, src, trg, col)
            C_, columns_ = comp.compare(data_src, data_trg)
            C += [C_]
            columns += columns_
        C = np.hstack(C)
        return C, columns


class Compare(object):
    def __init__(self):
        self.block = Block().load()
        self.prep = Preprocess().load()
        self.comp = _Compare()

    def compare(self):
        logger.debug("Starting comparison")
        C, columns = self.comp.compare(
            self.block.pairs, self.prep.src_df, self.prep.trg_df
        )
        return Comparison(C, columns)
