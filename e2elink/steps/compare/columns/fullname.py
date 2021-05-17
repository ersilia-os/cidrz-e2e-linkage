import numpy as np

from ..metrics.metrics import LevenshteinSimilarity, JaroWinklerSimilarity, MatchRatingApproach


class FullNameCompare(object):

    def __init__(self):
        self.metrics = [LevenshteinSimilarity(),
                        JaroWinklerSimilarity(),
                        MatchRatingApproach()]
        self.prefix = "full_name"
        self.dim = len(self.metrics)

    def compare(self, data_a, data_b):
        columns = []
        for metric in self.metrics:
            columns += [self.prefix + "_" + metric.label]
        C = []
        for a, b in zip(data_a, data_b):
            c = []
            for metric in self.metrics:
                c += [metric.calculate(a,b)]
            C += [c]
        C = np.array(C)
        results = {
            "C": C,
            "columns": columns
        }
        return results
