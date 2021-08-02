import joblib
import os
import csv
import json
import random

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

from .... import logger
from .... import DATA_PATH, MODELS_PATH

from ....synthetic.fakers.agegenerator import AgeGenerator
from ....synthetic.fakers.dategenerator import DateGenerator
from ....synthetic.fakers.namegenerator import NameGeneratorDefault
from ....synthetic.fakers.sexgenerator import SexGenerator


MAX_FEATURES = 1024
NGRAM_RANGE = (2, 2)
N = 10000

DATE_FORMATS = ["%Y-%m-%d", "%Y-%m-%d", "%d %b %Y", "%b %d %Y", "%d/%m/%y", "%d-%m-%y"]


class SchemaMatchingTrainer(object):
    def __init__(self):
        self.data_path = os.path.abspath(
            os.path.join(DATA_PATH, "schema_matcher_train.csv")
        )
        self.models_schema_path = os.path.join(os.path.abspath(MODELS_PATH), "schema")
        if not os.path.exists(self.models_schema_path):
            os.mkdir(self.models_schema_path)
        self.vectorizer_path = os.path.abspath(
            os.path.join(self.models_schema_path, "schema_matcher_vectorizer.pkl")
        )
        self.model_path = os.path.abspath(
            os.path.join(self.models_schema_path, "schema_matcher.pkl")
        )
        self.label_path = os.path.abspath(
            os.path.join(self.models_schema_path, "schema_matcher_labels.json")
        )

    @staticmethod
    def __random_date_format():
        return random.choice(DATE_FORMATS)

    def _generate_age(self):
        logger.debug("Generating ages")
        gen = AgeGenerator()
        R = []
        for _ in range(N):
            R += [
                (gen.sample(30, 15)["years"], "age")
            ]  #  Todo: this is just an example
        return R

    def _generate_names(self):
        logger.debug("Generating first names")
        gen = NameGeneratorDefault()
        R = []
        for _ in range(N):
            R += [(gen.first_name(), "first_name")]
        logger.debug("Generating last names")
        for _ in range(N):
            R += [(gen.last_name(), "last_name")]
        logger.debug("Generating full names")
        for _ in range(N):
            R += [(gen.full_name(), "full_name")]
        return R

    def _generate_dates(self):
        logger.debug("Generating visit dates")
        gen = DateGenerator()
        R = []
        for _ in range(N):
            R += [
                (
                    gen.sample("2016-01-01", "2020-12-31").strftime(
                        self.__random_date_format()
                    ),
                    "visit_date",
                )
            ]
        logger.debug("Generating birth dates")
        for _ in range(N):
            R += [
                (
                    gen.sample("1960-01-01", "2000-12-31").strftime(
                        self.__random_date_format()
                    ),
                    "birth_date",
                )
            ]
        return R

    def _generate_sexs(self):
        logger.debug("Generating sexs")
        gen = SexGenerator()
        R = []
        for _ in range(N):
            trunc = random.choice([True, False])
            sex = gen.sample()
            if trunc:
                R += [(sex[0], "sex")]
            else:
                R += [(sex, "sex")]
        return R

    def generate_dataset(self):
        logger.debug("Generating dataset and writing to {0}".format(self.data_path))
        R = []
        R += self._generate_age()
        R += self._generate_names()
        R += self._generate_sexs()
        R += self._generate_dates()
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
        labels = dict((l, i) for i, l in enumerate(labels))
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


def train():
    smt = SchemaMatchingTrainer()
    smt.generate_dataset()
    smt.vectorize()
    smt.fit()
