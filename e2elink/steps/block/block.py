from ...vectorize.namengrams import NameNgramVectorizer
from pysparnn import cluster_index as ci
import numpy as np


class Block(object):
    def __init__(self, pairs, k):
        self.pairs = pairs
        self.k = k
        self.label = "k{0}".format(str(k).zfill(3))

    def save(self):
        pass

    def load(self):
        pass


class Blocker(object):
    def __init__(self):
        self.vectorizer = NameNgramVectorizer()

    def _to_list(self, df):
        # TODO account for nan values
        R = []
        for r in df["full_name"].values:
            R += [str(r)]
        return R

    def block(self, src, trg, k=10):
        # TODO Mwansa
        # TODO Make this step smarter (include, for instance, identifiers)
        vec_src = self.vectorizer.vectorize(self._to_list(src), sparse=True)
        vec_trg = self.vectorizer.vectorize(self._to_list(trg), sparse=True)
        cp = ci.MultiClusterIndex(vec_trg, [i for i in range(0, len(trg))])
        res = np.array(cp.search(vec_src, k=k, return_distance=False), dtype=np.int)
        pairs = []
        for i, r in enumerate(res):
            for j in r:
                pairs += [(i, j)]
        pairs = np.array(pairs, dtype=np.int)
        return Block(pairs, k)
