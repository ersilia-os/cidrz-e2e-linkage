from sklearn.ensemble import RandomForestClassifier


class Model(object):
    def __init__(self):
        self.clf = RandomForestClassifier(class_weight="balanced", n_jobs=-1)

    def fit(self, comparisons, truth):
        X = comparisons.C
        y = truth
        self.clf.fit(X, y)
        self.columns = comparisons.columns

    def predict(self, comparisons):
        if comparisons.columns != self.columns.comparisons:
            return None
        X = comparisons.C
        y = self.clf.predict_proba(X)
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
