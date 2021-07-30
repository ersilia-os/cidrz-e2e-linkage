import os
import collections
import json
import pandas as pd

from ... import logger
from ..block.block import Block
from ..score.score import Score
from ..setup.setup import Session


SCORE_CUTOFF = 0.5

class Results(object):

    def __init__(self, results):
        self.results = results
        self.dataset_names = [k for k, _ in results.items()]
        self.path = os.path.join(Session().get_output_path(), "finish")
        self.names_path = os.path.join(self.path, "dataset_names.json")

    def save(self):
        logger.debug("A list of results datasets is stored at {0}".format(self.names_path))
        with open(self.names_path, "w") as f:
            json.dump(self.dataset_names, f, indent=4)
        for k, df in self.results.items():
            path = os.path.join(self.path, k+".csv")
            logger.debug("Saving results {0} in {1}".format(k, path))
            df.to_csv(path, index=False)

    def load(self):
        logger.debug("Reading dataset names from {0}".format(self.names_path))
        with open(self.names_path, "r") as f:
            dataset_names = json.load(f)
        results = {}
        for ds in dataset_names:
            path = os.path.join(self.path, ds+".csv")
            results[ds] = pd.read_csv(path)
        return Results(results)


class _Finisher(object):

    def __init__(self):
        self.columns = ["src_idx", "trg_idx", "score"]
        self.path = Session().get_output_path()

    def _best_per_src(self, pairs, score):
        src = collections.defaultdict(list)
        for r, s in zip(pairs, score):
            src[r[0]] += [(r[1], s)]
        keys = sorted([k for k,v in src.items()])
        R = []
        for k in keys:
            v = src[k]
            v = sorted(v, key = lambda x: -x[1])[0]
            R += [(k, v[0], v[1])]
        df = pd.DataFrame(R, columns=self.columns)
        return df

    def _pairs(self, pairs, score):
        R = []
        for r, s in zip(pairs, score):
            R += [(r[0], r[1], s)]
        df = pd.DataFrame(R, columns=self.columns)
        return df

    @staticmethod
    def _rename(df, sufix):
        rename = {}
        for c in list(df.columns):
            rename[c] = c + "__" + sufix
        return df.rename(columns = rename, inplace=False)

    @staticmethod
    def _filter(df, idxs):
        columns = list(df.columns)
        R = []
        for idx in list(idxs):
            R += [list(df.iloc[idx])]
        return pd.DataFrame(R, columns=columns)

    def _expand(self, df):
        path = os.path.join(self.path, "preprocess")
        src = pd.read_csv(os.path.join(path, "src.csv"))
        trg = pd.read_csv(os.path.join(path, "trg.csv"))
        df_src = self._filter(src, df["src_idx"])
        df_src = self._rename(df_src, "src")
        df_trg = self._filter(trg, df["trg_idx"])
        df_trg = self._rename(df_trg, "src")
        return pd.concat([df, df_src, df_trg], axis=1)

    def finish(self, pairs, score):
        df_0 = self._best_per_src(pairs, score)
        df_1 = self._pairs(pairs, score)
        df_2 = df_1[df_1["score"] >= SCORE_CUTOFF]
        results = {
            "best_per_src_idxs": df_0,
            "all_blocked_pairs_idxs": df_1,
            "selected_pairs_idxs": df_2,
            "best_per_src": self._expand(df_0),
            "all_blocked_pairs": self._expand(df_1),
            "selected_pairs": self._expand(df_1)
        }
        return results


class Finisher(object):

    def __init__(self):
        self.pairs = [(r[0], r[1]) for r in Block().load().pairs.values]
        self.score = Score().load().score
        self.finisher = _Finisher()

    def finish(self):
        results = self.finisher.finish(self.pairs, self.score)
        return Results(results)
