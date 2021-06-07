from pysparnn import cluster_index as ci
import numpy as np
import os
import json
import pandas as pd

from ... import logger
from ...vectorize.namengrams import NameNgramVectorizer
from ..preprocess.preprocess import Preprocess
from ..setup.setup import Session


class Block(object):
    def __init__(self, pairs=None, k=None):
        self.pairs = pairs
        self.k = k
        self.label = "k{0}".format(str(k).zfill(3))
        self.path = Session().get_output_path()
        self.pairs_file = os.path.join(self.path, "block", "pairs.csv")
        self.params_file = os.path.join(self.path, "block", "params.json")

    def save(self):
        self.pairs.to_csv(self.pairs_file, index=False)
        logger.debug("Blocking pairs saved to {0}".format(self.pairs_file))
        params = {"k": self.k}
        with open(self.params_file, "w") as f:
            json.dump(params, f, indent=4)
        logger.debug("Blocking parameters saved to {0}".format(self.params_file))

    def load(self):
        logger.debug("Reading blocking pairs from {0}".format(self.pairs_file))
        pairs = pd.read_csv(self.pairs_file)
        logger.debug("Reading blocking parameters from {0}".format(self.params_file))
        with open(self.params_file, "r") as f:
            params = json.load(f)
        return Block(pairs, params["k"])


class _Blocker(object):
    def __init__(self):
        self.vectorizer = NameNgramVectorizer()

    def _to_list(self, df):
        # TODO account for nan values
        #  TODO use more than the name
        R = []
        for r in df["full_name"].values:
            R += [str(r)]
        return R

    def block(self, src, trg, k):
        if k not in [5, 10, 100]:
            # for the moment, We only accepto k = 5, 10 or 100 (because of pre-trainede models)
            raise Exception
        # TODO Mwansa
        # TODO Make this step smarter (include, for instance, identifiers)
        logger.debug("Vectorizing source")
        vec_src = self.vectorizer.vectorize(self._to_list(src), sparse=True)
        logger.debug("Vectorizing target")
        vec_trg = self.vectorizer.vectorize(self._to_list(trg), sparse=True)
        logger.debug("Indexing")
        cp = ci.MultiClusterIndex(vec_trg, [i for i in range(0, len(trg))])
        logger.debug("Searching")
        res = np.array(cp.search(vec_src, k=k, return_distance=False), dtype=np.int)
        pairs = []
        for i, r in enumerate(res):
            for j in r:
                pairs += [(i, j)]
        pairs = np.array(pairs, dtype=np.int)
        logger.success("Successful blocking")
        return pairs


class Blocker(object):
    def __init__(self):
        self.prep = Preprocess().load()
        self.blocker = _Blocker()

    def block(self, k):
        pairs = self.blocker.block(self.prep.src_df, self.prep.trg_df, k=k)
        pairs = pd.DataFrame(pairs, columns=["src", "trg"])
        return Block(pairs, k)
