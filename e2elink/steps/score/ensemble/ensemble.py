import os
import joblib

from .... import logger
from ...setup.setup import Session


MAX_N = 10000


class Predictor(object):

    def __init__(self, mdl):
        self.mdl = mdl

    def predict(self, X):
        return self.mdl.predict_proba(X)[:, 1]


class ModelEnsembler(object):

    def __init__(self):
        this_mdl_path = os.path.join(Session().get_output_path(), "score", "mdl.pkl")
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

    def _scan_pretrained_models(self):
        # TODO: Based on pretrained models
        pass

    def _load_model(self, mdl_path):
        return joblib.load(mdl_path)

    def items(self):
        for mdl_path, w in zip(self.mdl_paths, self.weights):
            mdl = self._load_model(mdl_path)
            prd = Predictor(mdl)
            yield prd, w


"""
class ModelSampler(object):
    def __init__(self, data):
        if data.shape[0] > MAX_N:
            self.data = data.sample(n=MAX_N)
        else:
            self.data = data.sample(n=data.shape[0])
        self.models_path = os.path.join(MODELS_PATH, "linkage")
        self.checkpoints_path = os.path.join(self.models_path, "checkpoints")
        self.data_path = os.path.join(self.models_path, "data", "comparisons")

    def _load_data(self, identifier):
        df = pd.read_csv(
            os.path.join(self.data_path, identifier + ".tsv"), delimiter="\t"
        )
        if df.shape[0] > self.data.shape[0]:
            df = df.sample(n=self.data.shape[0])
        else:
            df = df.sample(n=self.df.shape[0])
        return df

    def _load_model(self, identifier):
        mdl = joblib.load(os.path.join(self.checkpoints_path, identifier + ".pkl"))
        return mdl

    def score_samples(self):
        scores = {}
        for fn in os.path.listdir(self.data_path):
            identifier = fn.split(".")[0]
            df = self._load_data(identifier)
            if df.shape[0] > self.data.shape[0]:
                data = self.data.sample(n=df.shape[0])
            else:
                data = self.data
            score = evaluation(data, df)
            scores[identifier] = score
        scores = sorted(scores.items(), key=lambda item: -item[1])
        return scores

    def sample(self, n):
        scores = self.score_samples()[:n]
        for identifier, score in scores:
            yield self._load_model(identifier), score
    """
