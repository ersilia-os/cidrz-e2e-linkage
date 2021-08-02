import os
import numpy as np
import json
import pandas as pd
import collections
from sklearn.metrics import roc_curve, auc, f1_score, precision_score, recall_score

from ... import logger
from ..setup.setup import Session
from ..score.score import Score
from ..block.block import Block

NULL = 0


class Evaluation(object):
    def __init__(self, res=None):
        self.res = res
        self.path = Session().get_output_path()
        self.res_path = os.path.join(self.path, "evaluate", "eval.json")

    def save(self):
        with open(self.res_path, "w") as f:
            json.dump(self.res, f, indent=4)
        logger.debug("Evaluation results stored at {0}".format(self.res_path))

    def load(self):
        logger.debug("Reading evaluation results from {0}".format(self.res_path))
        with open(self.res_path, "r") as f:
            res = json.load(f)
        return Evaluation(res=res)


class _Evaluator(object):
    def __init__(self):
        pass

    def evaluate(self, y_t, y_p):
        res = {}
        # Positives and negatives
        counts = {
            "pos": int(np.sum(y_t)),
            "neg": int(len(y_t) - np.sum(y_t)),
            "tot": int(len(y_t)),
        }
        res["counts"] = counts
        #  Area under the roc curve
        fpr, tpr, _ = roc_curve(y_t, y_p)
        res["auroc"] = auc(fpr, tpr)
        # Area under the precision recall curve
        #  Cutoff-specific (binary) metrics
        # TODO
        cuts = np.arange(0, 1, 0.01)
        y_p = np.array(y_p)
        scores = []
        f1 = []
        precision = []
        recall = []
        proportion = []
        for cut in cuts:
            scores += [cut]
            rep = {}
            y_p_ = np.zeros(len(y_p))
            y_p_[y_p >= cut] = 1
            proportion += [np.sum(y_p_) / len(y_p_)]
            if np.sum(y_p_) != 0:
                f1 += [f1_score(y_t, y_p_)]
                precision += [precision_score(y_t, y_p_)]
                recall += [recall_score(y_t, y_p_)]
            else:
                f1 += [NULL]
                precision += [NULL]
                recall += [NULL]
        res["score"] = scores
        res["f1"] = f1
        res["precision"] = precision
        res["recall"] = recall
        res["proportion"] = proportion
        return res


class _MetaEvaluator(object):
    def __init__(self):
        self.meta_path = os.path.join(Session().get_output_path(), "score", "meta.json")

    def evaluate(self):
        logger.debug(
            "Estimating performance from synthetic datasets {0}".format(self.meta_path)
        )
        with open(self.meta_path, "r") as f:
            meta = json.load(f)
        cv_results = meta["cv_results"]
        weights = meta["weights"]
        values = collections.defaultdict(list)
        for d in cv_results:
            for k, v in d.items():
                values[k] += [v]
        res = dict((k, np.average(v, weights=weights)) for k, v in values.items())
        return res


class Evaluator(object):
    def __init__(self):
        self.y = Score().load().score
        self.pairs = [(r[0], r[1]) for r in Block().load().pairs.values]
        self.truth_set = self._get_truth_set()
        self.evaluator = _Evaluator()
        self.metaevaluator = _MetaEvaluator()

    def _get_truth_set(self):
        truth_path = os.path.join(Session().get_output_path(), "raw", "truth.csv")
        if not os.path.exists(truth_path):
            logger.debug("No truth set available")
            return None
        df = pd.read_csv(truth_path)
        truth_set = set()
        for r in df.values:
            truth_set.update([(r[0], r[1])])
        logger.debug("Loaded truth from {0}".format(truth_path))
        return truth_set

    def _src_ys(self):
        y_t = []
        y_p = []
        src = set([r[0] for r in list(self.truth_set)])
        for i, pair in enumerate(self.pairs):
            if pair[0] not in src:
                continue
            if pair in self.truth_set:
                y_t += [1]
            else:
                y_t += [0]
            y_p += [self.y[i]]
        return y_t, y_p

    def _all_ys(self):
        y_t = []
        y_p = []
        for i, pair in enumerate(self.pairs):
            if pair in self.truth_set:
                y_t += [1]
            else:
                y_t += [0]
            y_p += [self.y[i]]
        return y_t, y_p

    def evaluate(self):
        if self.truth_set:
            logger.debug("Truth set available")
            y_t, y_p = self._src_ys()
            src_res = self.evaluator.evaluate(y_t, y_p)
            y_t, y_p = self._all_ys()
            all_res = self.evaluator.evaluate(y_t, y_p)
        else:
            logger.debug("Truth set not available")
            src_res = None
            all_res = None
        logger.debug("Metaevaluating")
        meta_res = self.metaevaluator.evaluate()
        res = {"src": src_res, "all": all_res, "meta": meta_res}
        return Evaluation(res=res)
