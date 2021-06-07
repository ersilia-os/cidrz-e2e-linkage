import os
import json
import numpy as np

from ... import logger
from ..setup.setup import Session
from ..compare.compare import Comparison


class Score(object):
    def __init__(self, score):
        self.score = score
        self.path = os.path.join(Session().get_output_path(), "score")
        self.score_path = os.path.join(self.path, "score.npy")

    def save(self):
        logger.debug("Scores saved to {0}".format(self.score_path))
        with open(self.score_path, "wb") as f:
            np.save(f, self.score, allow_pickle=False)

    def load(self):
        with open(self.score_path, "r") as f:
            score = np.load(f)
        logger.debug("Loading scores from {0}".format(self.score_path))
        return Score(score)


class _Scorer(object):
    def __init__(self):
        pass

    def _score(self, C):
        sc = np.sum(C, axis=1)
        return sc

    def score(self, C):
        sc = self._score(C)
        return sc


class Scorer(object):
    def __init__(self):
        self.C = Comparison().load().C
        self.scorer = _Scorer()

    def score(self):
        sc = self.scorer.score(self.C)
        return Score(sc)
