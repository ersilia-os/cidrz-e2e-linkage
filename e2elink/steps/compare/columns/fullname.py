import numpy as np

from ..metrics.metrics import (
    ExactSimilarity,
    LevenshteinSimilarity,
    JaroWinklerSimilarity,
    MatchRatingApproach,
    CosineSimilarity,
    MongeElkanLevenshteinSimilarity,
    MongeElkanJaroWinklerSimilarity
)

NULL = 0

class FullNameCompare(object):
    def __init__(self):
        self.metrics = [
            ExactSimilarity(),
            LevenshteinSimilarity(),
            JaroWinklerSimilarity(),
            MatchRatingApproach(),
            CosineSimilarity(),
            MongeElkanLevenshteinSimilarity(),
            MongeElkanJaroWinklerSimilarity()
        ]
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
                try:
                    v = metric.calculate(a, b)
                except:
                    v = NULL
                c += [v]
            C += [c]
        C = np.array(C)
        results = {"C": C, "columns": columns}
        return results
