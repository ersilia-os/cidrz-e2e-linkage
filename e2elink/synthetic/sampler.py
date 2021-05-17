import random
import uuid
import os
import pandas as pd

from .. import MODELS_PATH

from .tablegen.singletable import NaiveReferenceTableGenerator
from .tablegen.linkedtable import ReferenceLinkedTables, find_ground_truth
from .tablegen.transform import TableTransformer
from .utils.saver import save_results

from .misspell.simple import SimpleMisspell
from .misspell.embedding import EmbeddingMisspell

simple_misspell = SimpleMisspell()
embedding_misspell = None


def get_misspeller(name_misspelling_type):
    # TODO
    return SimpleMisspell()
    if name_misspelling_type == "Fast":
        if simple_misspell is None:
            simple_misspell = SimpleMisspell()
        ms = simple_misspell
    if name_misspelling_type == "Accurate":
        if embedding_misspell is None:
            embedding_misspell = EmbeddingMisspell()
        ms = embedding_misspell
    return ms


params = {
    "size": [100, 1000],
    "dupl": [0.01, 0.10],
    "visits": [1, 1.5],
    "sort_by_date": [True],
    "date_format": ["%Y-%m-%d"],
    "swap_full_name": [0.01, 0.10],
    "abbreviate_full_name": [0.01, 0.10],
    "misspell_full_name": [0.01, 0.10],
    "name_misspelling_type": ["Fast"],
    "age_format": ["birth_date"],
    "name_format": ["lower"],
    "split_full_name": [False],
    "shuffle_columns": [False],
    "hide_identifier": [False],
    "identifier_coverage": [0.01, 0.10, 0.25],
    "date_coverage": [0.90, 1.0],
    "name_coverage": [0.95, 1.0],
    "age_coverage": [0.8, 0.9, 1.0],
    "sex_format": ["lower_abbrv"],
    "header": [(0, 0)],
}

truth_params = {"exp_linkage_rate": [0.30, 0.50, 0.70, 0.90, 1.0]}


class SyntheticSampler(object):
    def __init__(self):
        self.data_path = os.path.join(MODELS_PATH, "linkage", "data", "raw")

    def _sample_params(self):
        params_ = {}
        for k, v in params.items():
            params_[k] = random.choice(v)
        params_["misspeller"] = get_misspeller(params_["name_misspelling_type"])
        return params_

    def _sample_truth_params(self):
        params_ = {}
        for k, v in truth_params.items():
            params_[k] = random.choice(v)
        return params_

    def _sample(self):
        src_params = self._sample_params()
        trg_params = self._sample_params()
        if src_params["size"] >= trg_params["size"]:
            return None
        # reference data
        truth_params = self._sample_truth_params()
        src_gen = NaiveReferenceTableGenerator(src_params)
        trg_gen = NaiveReferenceTableGenerator(trg_params)
        lt = ReferenceLinkedTables(src_gen, trg_gen)
        ref_data = lt.sample(
            src_params["size"], trg_params["size"], truth_params["exp_linkage_rate"]
        )
        # source file
        src_tf = TableTransformer(ref_data["src"])
        src_tf.transform(src_params)
        src_uid = src_tf.uid
        src_data = src_tf.data.copy()
        # target file
        trg_tf = TableTransformer(ref_data["trg"])
        trg_tf.transform(trg_params)
        trg_uid = trg_tf.uid
        trg_data = trg_tf.data.copy()
        # likage file
        pairs = find_ground_truth(src_uid, trg_uid)
        results = {
            "src_data": src_data,
            "trg_data": trg_data,
            "pairs": pairs,
            "src_params": src_params,
            "trg_params": trg_params,
            "truth_params": truth_params,
        }
        return results

    def sample(self, n):
        done = 0
        while done < n:
            identifier = str(uuid.uuid4())
            res = self._sample()
            if res is None:
                continue
            save_results(
                self.data_path,
                identifier,
                res["src_data"],
                res["trg_data"],
                res["pairs"],
                res["src_params"],
                res["trg_params"],
                res["truth_params"],
            )
            done += 1

    def load(self, identifier):
        dir = os.path.join(self.data_path, identifier)
        src = pd.read_csv(os.path.join(dir, "source.tsv"), delimiter="\t")
        trg = pd.read_csv(os.path.join(dir, "target.tsv"), delimiter="\t")
        truth = pd.read_csv(os.path.join(dir, "truth.tsv"), delimiter="\t")
        return {"src": src, "trg": trg, "truth": truth}
