from ....metrics.metrics import (
    ExactSimilarity,
    LevenshteinSimilarity,
    JaroWinklerSimilarity,
    MatchRatingApproach,
    CosineSimilarity,
    MongeElkanLevenshteinSimilarity,
    MongeElkanJaroWinklerSimilarity,
)

from ....columns.full_name import FullNameColumn


class FullNameMetrics(object):
    def __init__(self):
        self.metrics = [
            ExactSimilarity(),
            LevenshteinSimilarity(),
            JaroWinklerSimilarity(),
            MatchRatingApproach(),
            CosineSimilarity(),
            # MongeElkanLevenshteinSimilarity(),
            # MongeElkanJaroWinklerSimilarity()
        ]
        self.prefix = FullNameColumn().label
