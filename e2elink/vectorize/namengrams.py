import os
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer

from .. import MODELS_PATH
from ..synthetic.fakers.namegenerator import NameGeneratorDefault, NameGenerator


MAX_FEATURES = 200
NGRAM_RANGE = (2, 2)

MAX_DATA = 10000


class NameNgramVectorizer(object):
    def __init__(self):
        self.model_path = os.path.join(MODELS_PATH, "name_ngram.pkl")
        if os.path.exists(self.model_path):
            self.mdl = joblib.load(self.model_path)
        else:
            self.mdl = None

    def fit(self):
        data = []
        n = int(MAX_DATA / 4)
        ng = NameGeneratorDefault()
        data += [ng.full_name(sex="f") for _ in range(n)]
        data += [ng.full_name(sex="m") for _ in range(n)]
        ng = NameGenerator()
        data += [ng.full_name(sex="f") for _ in range(n)]
        data += [ng.full_name(sex="m") for _ in range(n)]
        mdl = TfidfVectorizer(
            analyzer="char_wb", ngram_range=NGRAM_RANGE, max_features=MAX_FEATURES
        )
        mdl.fit(data)
        joblib.dump(mdl, self.model_path)
        self.mdl = mdl

    def vectorize(self, words, sparse=False):
        v = self.mdl.transform(words)
        if sparse:
            return v
        else:
            return v.toarray()
