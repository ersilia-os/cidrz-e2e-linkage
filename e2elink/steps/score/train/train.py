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
        self.mdl = CalibratedClassifierCV(self.base_clf)

    def fit(self, X, y):
        idxs = [i for i in range(len(y))]
        idxs = idxs.shuffle()
        idxs = idxs[:MAX_N]
        self.mdl.fit(X[idxs], y[idxs])


class Model(object):

    def __init__(self, mdl=None):
        self.mdl = mdl
        self.path = os.path.join(Session().get_output_path(), "score")
        self.mdl_path = os.path.join(self.path, "mdl.pkl")

    def save(self):
        joblib.dump(self.mdl, self.mdl_path)
        logger.debug("Model saved to {0}".format(self.mdl_path))

    def load(self):
        logger.debug("Loading model from {0}".format(self.mdl_path))
        mdl = joblib.load(self.mdl_path)


class _ModelTrainer(object):

    def __init__(self):
        self.mdl = _Model()

    def fit(self, C, y):
        self.mdl.fit(C, y)
        return self.mdl


class ModelTrainer(object):

    def __init__(self):
        y_path = os.path.join(Session().get_output_path(), "block", "y.npy")
        if os.path.exists(y_path):
            self.C = Comparison().load().C
            self.y = Block().load().y
            self.trainer = _ModelTrainer()
        else:
            self.trainer = None

    def fit(self):
        if self.trainer is None:
            return None
        logger.debug("Training model")
        mdl = self.trainer.fit(self.C, self.y)
        return Model(mdl)
