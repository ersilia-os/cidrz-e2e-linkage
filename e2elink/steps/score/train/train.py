from sklearn.ensemble import RandomForestClassifier
from sklearn.calibration import CalibratedClassifierCV

MAX_N = 10000


class Model(object):
    def __init__(self):
        self.base_clf = RandomForestClassifier(class_weight="balanced", n_jobs=-1)
        self.clf = CalibratedClassifierCV(self.base_clf)

    @staticmethod
    def _get_y_from_truth(comparisons, truth):
        pairs = comparisons.pairs
        truth_set = set([(x[0], x[1]) for x in truth])
        y = np.zeros((len(pairs),), dtype=np.int)
        for i, p in enumerate(pairs):
            if p in truth_set:
                y[i] = 1
        return y

    def fit(self, comparisons, truth):
        X = comparisons.C
        y = truth
        idxs = [i for i in range(len(y))]
        idxs = idxs.shuffle()
        idxs = idxs[:MAX_N]
        self.clf.fit(X[idxs], y[idxs])
        self.columns = comparisons.columns

    def predict(self, comparisons):
        if comparisons.columns != self.columns.comparisons:
            return None
        X = comparisons.C
        y = self.clf.predict_proba(X)[:, 1]
        return y

    def save(self):
        pass

    def load(self):
        pass


class LinkageModelTrainer(object):
    def __init__(self, identifier):
        pass

    def foo(self):
        pass
