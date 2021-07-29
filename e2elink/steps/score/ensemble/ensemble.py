import os
import joblib

import numpy as np
import scipy.stats

from .... import logger
from ...setup.setup import Session
from ....vars import MODELS_PATH


MAX_N = 10000


class Predictor(object):

    def __init__(self, mdl):
        self.mdl = mdl

    def predict(self, X):
        return self.mdl.predict_proba(X)[:, 1]


class DistributionDistances(object):

    def __init__(self, p, q):
        self.p = np.array(p)
        self.q = np.array(q)

    def jensen_shannon_distance(self):
        p = self.p
        q = self.q
        m = (p + q) / 2
        divergence = (scipy.stats.entropy(p, m) + scipy.stats.entropy(q, m)) / 2
        distance = np.sqrt(divergence)
        return distance


class ModelEnsembler(object):

    def __init__(self):
        self.output_path = Session().get_output_path()
        self.tags_path = os.path.join(MODELS_PATH, "linkage", "results")
        this_mdl_path = os.path.join(self.output_path, "score", "mdl.pkl")
        if os.path.exists(this_mdl_path):
            logger.debug("Model exists for this dataset")
            self.mdl_paths = [this_mdl_path]
            self.weights = [1.]
            self.has_mdl = True
        else:
            logger.debug("Model does not exist for this dataset")
            self.mdl_paths = []
            self.weights = []
            self.has_mdl = False
        self._scan_pretrained_models()

    def _read_columns(self, path):
        with open(os.path.join(path, "compare", "columns.json"), "r") as f:
            columns = json.load(f)
        return columns

    def _read_C(self, path):
        with open(os.path.join(path, "compare", "C.npy"), "rb") as f:
            C = np.load(f)
        return C

    def _find_pretrained_models_with_same_columns(self):
        columns = self._read_columns(self.output_path)
        for tag in os.listdir(self.tags_path):
            if len(tag) != 36:
                continue
            pretrained_columns = self._read_columns(os.path.join(self.tags_path, tag))
            if columns != pretrained_columns:
                continue
            yield tag

    def _measure_C_coincidence(self, C_0, C_1):
        pass

    def _scan_pretrained_models(self):
        C_0 = self._read_C(self.output_path)
        for tag in self._find_pretrained_models_with_same_columns():
            C_1 = self._read_C(os.path.join(self.tags_path, tag))
            coincidence = self._measure_C_coincidence(C_0, C_1)
        # TODO: Based on pretrained models
        pass

    def _load_model(self, mdl_path):
        return joblib.load(mdl_path)

    def items(self):
        for mdl_path, w in zip(self.mdl_paths, self.weights):
            mdl = self._load_model(mdl_path)
            prd = Predictor(mdl)
            yield prd, w
