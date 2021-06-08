import os
import json
import numpy as np

from ... import logger
from .train.train import ModelTrainer
from .ensemble.ensemble import ModelEnsembler
from ..setup.setup import Session
from ..compare.compare import Comparison


class Score(object):
    def __init__(self, score=None):
        self.score = score
        self.path = os.path.join(Session().get_output_path(), "score")
        self.score_path = os.path.join(self.path, "score.npy")

    def save(self):
        logger.debug("Scores saved to {0}".format(self.score_path))
        with open(self.score_path, "wb") as f:
            np.save(f, self.score, allow_pickle=False)

    def load(self):
        with open(self.score_path, "rb") as f:
            score = np.load(f)
        logger.debug("Loading scores from {0}".format(self.score_path))
        return Score(score)


class _Scorer(object):
    def __init__(self, ensembler):
        self.ensembler = ensembler

    def _score(self, C):
        P = []
        W = []
        for mdl, w in self.ensembler.items():
            P += [mdl.predict(C)]
            W += [w]
        P = np.array(P).T
        sc = np.average(P, axis=1, weights=W)
        return sc

    def score(self, C):
        sc = self._score(C)
        return sc


class Scorer(object):
    def __init__(self):
        self.C = Comparison().load().C
        self._fit_if_available()
        self.ensembler = ModelEnsembler()
        self.scorer = _Scorer(self.ensembler)

    def _fit_if_available(self):
        mdl = ModelTrainer().fit()
        if mdl is not None:
            mdl.save()

    def score(self):
        sc = self.scorer.score(self.C)
        return Score(sc)
