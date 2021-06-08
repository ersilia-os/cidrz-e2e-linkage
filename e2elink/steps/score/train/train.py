import os
import random
import joblib
import json
import numpy as np

from sklearn.ensemble import RandomForestClassifier
from sklearn.calibration import CalibratedClassifierCV

from .... import logger
from ...setup.setup import Session
from ...compare.compare import Comparison
from ...block.block import Block


MAX_N = 10000


class _Model(object):
    def __init__(self):
        self.base_mdl = RandomForestClassifier(class_weight="balanced", n_jobs=-1)
        self.mdl = CalibratedClassifierCV(self.base_mdl)

    def fit(self, X, y):
        idxs = [i for i in range(len(y))]
        random.shuffle(idxs)
        idxs = idxs[:MAX_N]
        self.mdl.fit(X[idxs], y[idxs])


class Model(object):

    def __init__(self, mdl=None, train_C=None, train_columns=None):
        self.mdl = mdl
        self.path = os.path.join(Session().get_output_path(), "score")
        self.mdl_path = os.path.join(self.path, "mdl.pkl")
        self.train_C = train_C
        self.train_columns = train_columns
        self.train_C_path = os.path.join(self.path, "train_C.npy")
        self.train_columns_path = os.path.join(self.path, "train_columns.json")

    def save(self):
        joblib.dump(self.mdl, self.mdl_path)
        logger.debug("Model saved to {0}".format(self.mdl_path))
        with open(self.train_C_path, "wb") as f:
            np.save(f, self.train_C)
        logger.debug("Model train data saved to {0}".format(self.train_C_path))
        with open(self.train_columns_path, "w") as f:
            json.dump(self.train_columns, f, indent=4)

    def load(self):
        logger.debug("Loading model from {0}".format(self.mdl_path))
        mdl = joblib.load(self.mdl_path)
        logger.debug("Loading train data from {0}".format(self.train_C_path))
        with open(self.train_C_path, "rb") as f:
            train_C = np.load(f)
        logger.debug("Loading train columns from {0}".format(self.train_columns_path))
        with open(self.train_columns_path, "r") as f:
            train_columns = json.load(f)
        return Model(mdl=mdl, train_C=train_C, train_columns=train_columns)


class _ModelTrainer(object):

    def __init__(self):
        self.mdl = _Model()

    def fit(self, C, y):
        mask = ~np.isnan(y)
        C = C[mask]
        y = y[mask]
        self.mdl.fit(C, y)
        return self.mdl.mdl, C, y


class ModelTrainer(object):

    def __init__(self):
        y_path = os.path.join(Session().get_output_path(), "block", "y.npy")
        if os.path.exists(y_path):
            comp = Comparison().load()
            self.C = comp.C
            self.columns = comp.columns
            self.y = Block().load().y
            self.trainer = _ModelTrainer()
        else:
            self.trainer = None

    def fit(self):
        if self.trainer is None:
            return None
        logger.debug("Training model")
        mdl, C, y = self.trainer.fit(self.C, self.y)
        return Model(mdl, C, self.columns)
