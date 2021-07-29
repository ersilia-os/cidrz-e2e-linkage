"""
This script is currently very dirty and needs a lot of refactoring.
"""
import joblib
import os
import csv
import json

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

from .... import logger
from .... import DATA_PATH, MODELS_PATH

from ....synthetic.fakers.agegenerator import AgeGenerator
from ....synthetic.fakers.dategenerator import DateGenerator
from ....synthetic.fakers.namegenerator import NameGeneratorDefault


MAX_FEATURES = 1024
NGRAM_RANGE = (2, 2)
N = 10000


class SchemaMatchingTrainer(object):

    def __init__(self):
        self.data_path = os.path.abspath(os.path.join(DATA_PATH, "schema_matcher_train.csv"))
        self.vectorizer_path = os.path.abspath(os.path.join(MODELS_PATH, "schema_matcher_vectorizer.pkl"))
        self.model_path = os.path.abspath(os.path.join(MODELS_PATH, "schema_matcher.pkl"))
        self.label_path = os.path.abspath(os.path.join(MODELS_PATH, "schema_matcher_labels.json"))

    def generate_dataset(self):
        logger.debug("Generating dataset and writing to {0}".format(self.data_path))
        R = []
        logger.debug("Generating ages")
        gen = AgeGenerator()
        for _ in range(N):
            R += [(gen.sample(30, 15)["years"], "age")] # Todo: this is just an example
        logger.debug("Generating first names")
        gen = NameGeneratorDefault()
        for _ in range(N):
            R += [(gen.first_name(), "first_name")]
        logger.debug("Generating last names")
        for _ in range(N):
            R += [(gen.last_name(), "last_name")]
        logger.debug("Generating full names")
        for _ in range(N):
            R += [(gen.full_name(), "full_name")]
        logger.debug("Generating visit dates")
        gen = DateGenerator()
        for _ in range(N):
            R += [(gen.sample("2016-01-01", "2020-12-31").strftime("%Y-%m%d"), "visit_date")]
        logger.debug("Generating birth dates")
        for _ in range(N):
            R += [(gen.sample("1960-01-01", "2000-12-31").strftime("%Y-%m%d"), "birth_date")]
        logger.debug("Writing results")
        with open(self.data_path, "w") as f:
            for r in R:
                f.write("{0},{1}".format(r[0], r[1]) + os.linesep)

    def vectorize(self):
        logger.debug("Reading values")
        with open(self.data_path, "r") as f:
            reader = csv.reader(f)
            data = []
            for r in reader:
                data += [r[0]]
        mdl = TfidfVectorizer(
            analyzer="char_wb", ngram_range=NGRAM_RANGE, max_features=MAX_FEATURES
        )
        mdl.fit(data)
        logger.debug("Saving vecorizer to {0}".format(self.vectorizer_path))
        joblib.dump(mdl, self.vectorizer_path)

    def fit(self):
        logger.debug("Fitting")
        logger.debug("Loading vectorizer")
        vec = joblib.load(self.vectorizer_path)
        logger.debug("Reading data")
        labels = set()
        with open(self.data_path, "r") as f:
            reader = csv.reader(f)
            for r in reader:
                labels.update([r[1]])
        labels = sorted(labels)
        labels = dict((l, i) for i,l in enumerate(labels))
        logger.debug("Saving labels to {0}".format(self.label_path))
        with open(self.label_path, "w") as f:
            json.dump(labels, f, indent=4)
        logger.debug("Getting vectorized data")
        with open(self.data_path, "r") as f:
            reader = csv.reader(f)
            data = []
            for r in reader:
                data += [r[0]]
        X = vec.transform(data)
        logger.debug("Getting y data")
        y = []
        with open(self.data_path, "r") as f:
            reader = csv.reader(f)
            y = []
            for r in reader:
                y += [labels[r[1]]]
        logger.debug("Training")
        mdl = MultinomialNB()
        mdl.fit(X, y)
        logger.debug("Saving model to {0}".format(self.model_path))
        joblib.dump(mdl, self.model_path)


if __name__ == "__main__":
    smt = SchemaMatchingTrainer()
    smt.generate_dataset()
    smt.vectorize()
    smt.fit()
