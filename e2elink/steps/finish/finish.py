import os
import collections
import pandas as pd

from ... import logger
from ..block.block import Block
from ..score.score import Score
from ..setup.setup import Session


class Results(object):

    def __init__(self, df_scored=None, df_best=None):
        self.df_scored = df_scored
        self.df_best = df_best
        self.path = Session().get_output_path()
        self.df_scored_path = os.path.join(self.path, "scored_matches.csv")
        self.df_best_path = os.path.join(self.path, "best_matches.csv")

    def save(self):
        self.df_scored.to_csv(self.df_scored_path, index=False)
        logger.debug("Saved scored matches to {0}".format(self.df_scored_path))
        self.df_best.to_csv(self.df_best_path, index=False)
        logger.debug("Saved best matches to {0}".format(self.df_best_path))

    def load(self):
        logger.debug("Reading scored matches from {0}".format(self.df_scored_path))
        df_scored = pd.read_csv(self.df_scored_path)
        logger.debug("Reading best matches from {0}".format(self.df_best_path))
        df_best = pd.read_csv(self.df_best_path)
        return Results(df_scored, df_best)


class _Finisher(object):

    def __init__(self):
        self.columns = ["src_idx", "trg_idx", "score"]

    def _best_per_src(self, pairs, score):
        src = collections.defaultdict(list)
        for r, s in zip(pairs, score):
            src[r[0]] += [(r[1], s)]
        keys = sorted([k for k,v in src.items()])
        R = []
        for k in keys:
            v = src[k]
            v = sorted(v, key = lambda x: -x[1])[0]
            R += [(k, v[0], v[1])]
        df = pd.DataFrame(R, columns=self.columns)
        return df

    def _pairs(self, pairs, score):
        # TODO: decide a cutoff
        R = []
        for r, s in zip(pairs, score):
            R += [(r[0], r[1], s)]
        df = pd.DataFrame(R, columns=self.columns)
        return df

    def finish(self, pairs, score):
        df_b = self._best_per_src(pairs, score)
        df_p = self._pairs(pairs, score)
        return df_b, df_p


class Finisher(object):

    def __init__(self):
        self.pairs = [(r[0], r[1]) for r in Block().load().pairs.values]
        self.score = Score().load().score
        self.finisher = _Finisher()

    def finish(self):
        df_best, df_scored = self.finisher.finish(self.pairs, self.score)
        return Results(df_scored, df_best)
