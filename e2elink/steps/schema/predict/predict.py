import joblib
import json
import os
from statistics import mode

from .... import logger
from .... import MODELS_PATH


COLUMN_SYNONYMS = {
    "identifier": ["client id", "number", "unique id"],
    "full_name": ["name", "full name", "client name", "client"],
    "first_name": [
        "first name",
        "given name",
    ],
    "last_name": ["family name", "surname", "last name"],
    "sex": ["gender"],
    "birth_date": [
        "date of birth",
        "birthdate",
    ],
    "birth_year": ["year of birth", "birthyear"],
    "age": [],
    "visit_date": ["visit date", "date of visit", "date"],
    "entry_date": ["entry date", "date of entry"],
    "clinical_variable": ["hiv", "via", "hiv status", "via status"],
}


class SchemaMatchingPredictor(object):
    def __init__(self):
        self.models_schema_path = os.path.join(os.path.abspath(MODELS_PATH), "schema")
        self.vectorizer_path = os.path.join(self.models_schema_path, "schema_matcher_vectorizer.pkl")
        self.model_path = os.path.join(self.models_schema_path, "schema_matcher.pkl")
        self.label_path = os.path.join(self.models_schema_path, "schema_matcher_labels.json")
        self.vec = joblib.load(self.vectorizer_path)
        self.mdl = joblib.load(self.model_path)
        with open(self.label_path, "r") as f:
            self.labels = json.load(f)
        self.label_inv = dict((v, k) for k, v in self.labels.items())

    def _predict(self, data):
        X = self.vec.transform(data)
        y = self.mdl.predict(X)
        return y

    def predict(self, data):
        y = self._predict(data)
        v = mode(y)
        return self.label_inv[v]


class SchemaMatchingSynonyms(object):

    def __init__(self):
        self.synonyms_inv = dict((x, k) for k, v in COLUMN_SYNONYMS.items() for x in v + [k])

    def predict(self, column):
        column = column.lower()
        if column in self.synonyms_inv:
            return self.synonyms_inv[column]
        else:
            return None
