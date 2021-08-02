import joblib
import json
import os

from .... import logger
from .... import MODELS_PATH


class SchemaMatchingPredictor(object):
    def __init__(self):
        self.vectorizer_path = os.path.abspath(
            os.path.join(MODELS_PATH, "schema_matcher_vectorizer.pkl")
        )
        self.model_path = os.path.abspath(
            os.path.join(MODELS_PATH, "schema_matcher.pkl")
        )
        self.label_path = os.path.abspath(
            os.path.join(MODELS_PATH, "schema_matcher_labels.json")
        )
        self.vec = joblib.load(self.vectorizer_path)
        self.mdl = joblib.load(self.model_path)
        with open(self.label_path, "r") as f:
            self.labels = json.load(f)
        self.label_inv = dict((v, k) for k, v in self.labels.items())

    def predict(self, data):
        X = self.vec.transform(data)
        y_ = self.mdl.predict(X)
        y = []
        for val in y_:
            y += [self.label_inv[val]]
        return y
