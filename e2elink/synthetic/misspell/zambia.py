import os
import pickle
import csv
import collections
import random
from ... import DATA_PATH, MODELS_PATH


class ZambiaMisspell(object):

    def __init__(self):
        self.script_path       = os.path.dirname(os.path.realpath(__file__))
        self.data_path         = os.path.join(DATA_PATH, "zambia_names_manual.tsv")
        self.data_path_name    = os.path.join(DATA_PATH, "some_curated_zambia_names.tsv")
        self.data_path_surname = os.path.join(DATA_PATH, "some_curated_zambia_surnames.tsv")
        self.model_path        = os.path.join(MODELS_PATH, "curated_zambia_names.pkl")
        if os.path.exists(self.model_path):
            with open(self.model_path, "rb") as f:
                d = pickle.load(f)
                self.pairs = d[0]
                self.pairs_neg = d[1]

    def fit(self):
        pairs = collections.defaultdict(list)
        pairs_neg = collections.defaultdict(list)
        with open(self.data_path, "r") as f:
            for r in csv.reader(f, delimiter="\t"):
                if len(r) < 3: continue
                if r[2] == "2":
                    pairs[r[0]] += [r[1]]
                    pairs[r[1]] += [r[0]]
                if r[2] == "1":
                    pairs_neg[r[0]] += [r[1]]
                    pairs_neg[r[1]] += [r[0]]
        with open(self.data_path_name, "r") as f:
            for r in csv.reader(f, delimiter="\t"):
                if len(r) < 3: continue
                if r[2] == "2":
                    pairs[r[0]] += [r[1]]
                    pairs[r[1]] += [r[0]]
                if r[2] == "1":
                    pairs_neg[r[0]] += [r[1]]
                    pairs_neg[r[1]] += [r[0]]
        with open(self.data_path_surname, "r") as f:
            for r in csv.reader(f, delimiter="\t"):
                if len(r) < 3: continue
                if r[2] == "2":
                    pairs[r[0]] += [r[1]]
                    pairs[r[1]] += [r[0]]
                if r[2] == "1":
                    pairs_neg[r[0]] += [r[1]]
                    pairs_neg[r[1]] += [r[0]]
        self.pairs = pairs
        self.pairs_neg = pairs_neg
        with open(self.model_path, "wb") as f:
            pickle.dump((pairs, pairs_neg), f)

    def misspell(self, word, n):
        if word in self.pairs:
            cands = self.pairs[word]
            cands = random.sample(cands, min(len(cands), n))
            return cands
        else:
            return None
