"""MOE misspelling"""

import os
import csv
import collections
import random
import numpy as np
import pickle
from fuzzywuzzy import fuzz
from tqdm import tqdm
from ... import DATA_PATH, MODELS_PATH


MAX = 50


class MoeMisspell(object):
    def __init__(self):
        self.script_path = os.path.dirname(os.path.realpath(__file__))
        self.data_path = os.path.join(DATA_PATH, "moe_misspellings_train.tsv")
        self.model_path = os.path.join(MODELS_PATH, "moe_misspellings_train.pkl")
        if os.path.exists(self.model_path):
            with open(self.model_path, "rb") as f:
                d = pickle.load(f)
            self.good2bad = d[0]
            self.bad2good = d[1]

    def fit(self):
        good2bad = collections.defaultdict(list)
        bad2good = collections.defaultdict(list)
        with open(self.data_path, "r") as f:
            reader = csv.reader(f, delimiter="\t")
            for r in tqdm(reader):
                good2bad[r[1]] += [r[0]]
                bad2good[r[0]] += [r[1]]
        with open(self.model_path, "wb") as f:
            d = (good2bad, bad2good)
            pickle.dump(d, f)
        self.good2bad = good2bad
        self.bad2good = bad2good

    def _returner(self, word, v, n, sort):
        if not sort:
            return random.sample(v, min(n, len(v)))
        else:
            levs = np.array([fuzz.ratio(w, word) for w in v])
            idxs = np.argsort(-levs)
            return list(np.array(v)[idxs][:n])

    def misspell(self, word, n, sort=True):
        if word in self.good2bad:
            v = list(set(self.good2bad[word]))
            if len(v) > MAX:
                v = random.sample(v, MAX)
            return self._returner(word, v, n, sort)
        else:
            return None

    def correct(self, word, n, sort=True):
        if word in self.bad2good:
            v = list(set(self.bad2good[word]))
            return self._returner(word, v, n, sort)
        else:
            return None
