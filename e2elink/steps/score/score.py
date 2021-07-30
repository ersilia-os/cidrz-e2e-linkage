import os
import json
import numpy as np

from ... import logger
from .train.train import ModelTrainer
from .ensemble.ensemble import ModelEnsembler
from ..setup.setup import Session
from ..compare.compare import Comparison


class Score(object):
    def __init__(self, score=None, meta=None):
        self.score = score
        self.meta = meta
        self.path = os.path.join(Session().get_output_path(), "score")
        self.score_path = os.path.join(self.path, "score.npy")
        self.meta_path = os.path.join(self.path, "meta.json")

    def save(self):
        logger.debug("Scores saved to {0}".format(self.score_path))
        with open(self.score_path, "wb") as f:
            np.save(f, self.score, allow_pickle=False)
        logger.debug("Metadata saved to {0}".format(self.meta_path))
        with open(self.meta_path, "w") as f:
            json.dump(self.meta, f, indent=4)

    def load(self):
        with open(self.score_path, "rb") as f:
            score = np.load(f)
        logger.debug("Loading scores from {0}".format(self.score_path))
        with open(self.meta_path, "r") as f:
            meta = json.load(f)
        logger.debug("Loading metadata from {0}".format(self.meta_path))
        return Score(score, meta)


class _Scorer(object):
    def __init__(self, ensembler):
        self.ensembler = ensembler

    def _score(self, C):
        P = []
        W = []
        CV = []
        T = []
        for item in self.ensembler.items():
            tag = item["tag"]
            mdl = item["predictor"]
            w = item["weight"]
            cv = item["cv_results"]
            P += [mdl.predict(C)]
            W += [w]
            CV += [cv]
            T += [tag]
        P = np.array(P).T
        sc = np.average(P, axis=1, weights=W)
        meta = {
            "tags": T,
            "cv_results": CV,
            "weights": W
        }
        return sc, meta

    def score(self, C):
        sc, meta = self._score(C)
        return sc, meta


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
        sc, meta = self.scorer.score(self.C)
        return Score(sc, meta)
