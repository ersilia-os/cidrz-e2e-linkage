import os
import pandas as pd
import numpy as np
from svd import evaluation
import joblib
from .. import MODELS_PATH

MAX_N = 10000


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
        """Return top n samples"""
        scores = self.score_samples()[:n]
        for identifier, score in scores:
            yield self._load_model(identifier), score
