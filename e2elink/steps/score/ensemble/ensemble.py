import os
import json
import joblib

import numpy as np
from scipy.stats import rankdata
import scipy.stats
from sklearn.metrics import mean_squared_error

from .... import logger
from ...setup.setup import Session
from .... import MODELS_PATH


MAX_N = 10


class Predictor(object):
    def __init__(self, mdl):
        self.mdl = mdl

    def predict(self, X):
        return self.mdl.predict_proba(X)[:, 1]


class DistributionCoincidence(object):
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

    def mean_squared_error(self):
        p = sorted(self.p)
        q = sorted(self.q)
        mse = mean_squared_error(p, q)
        return mse


class ModelEnsembler(object):
    def __init__(self):
        self.output_path = Session().get_output_path()
        self.tags_path = os.path.join(MODELS_PATH, "linkage", "results")
        this_mdl_path = os.path.join(self.output_path, "score", "mdl.pkl")
        if os.path.exists(this_mdl_path):
            logger.debug("Model exists for this dataset")
            self.mdl_paths = [this_mdl_path]
            self.weights = [1.0]
            self.has_mdl = True
        else:
            logger.debug("Model does not exist for this dataset")
            self.mdl_paths = []
            self.weights = []
            self.has_mdl = False

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
        values = []
        n = np.min([C_0.shape[0], C_1.shape[1]])
        idxs_0 = np.random.choice(C_0.shape[0], n, replace=False)
        idxs_1 = np.random.choice(C_1.shape[1], n, replace=False)
        for i in range(C_0.shape[1]):
            p = C_0[:, i]
            q = C_1[:, i]
            p = p[idxs_0]
            q = q[idxs_1]
            values += [DistributionCoincidence(p, q).mean_squared_error()]
        return np.array(values)

    def _scan_pretrained_models(self):
        logger.debug("Scan pretrained models")
        C_0 = self._read_C(self.output_path)
        R = []
        tags = []
        for tag in self._find_pretrained_models_with_same_columns():
            C_1 = self._read_C(os.path.join(self.tags_path, tag))
            coincidence = self._measure_C_coincidence(C_0, C_1)
            R += [coincidence]
            tags += [tag]
        R = np.array(R)
        X = np.zeros(R.shape)
        for i in range(R.shape[1]):
            r = rankdata(R[:, i], method="ordinal")
            X[:, i] = r / np.max(r)
        S = np.median(X, axis=1)
        idxs = np.argsort(S)[:MAX_N]
        tags = [tags[i] for i in idxs]
        scores = [len(idxs) - i for i in range(len(idxs))]  #  TODO: Refine score
        scores = np.array(scores) / np.max(scores)
        for tag, score in zip(tags, scores):
            yield tag, score

    def _load_model_by_tag(self, tag):
        tag_path = os.path.join(self.tags_path, tag)
        mdl_path = os.path.join(tag_path, "score", "mdl.pkl")
        mdl = joblib.load(mdl_path)
        return mdl

    def _load_cv_results_by_tag(self, tag):
        tag_path = os.path.join(self.tags_path, tag)
        cv_results_path = os.path.join(tag_path, "score", "cv_results.json")
        with open(cv_results_path, "r") as f:
            cv_results = json.load(f)
        return cv_results

    def items(self):
        for tag, score in self._scan_pretrained_models():
            mdl = self._load_model_by_tag(tag)
            cv_results = self._load_cv_results_by_tag(tag)
            prd = Predictor(mdl)
            results = {
                "tag": tag,
                "predictor": prd,
                "weight": score,
                "cv_results": cv_results,
            }
            yield results
