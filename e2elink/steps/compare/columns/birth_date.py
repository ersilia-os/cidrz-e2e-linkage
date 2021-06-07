from ..metrics.metrics import LevenshteinSimilarity, TimeDaysSimilarity

from ..columns import BirthDateColumn


class BirthDateMetrics(object):
    def __init__(self):
        self.metrics = [LevenshteinSimilarity(), TimeDaysSimilarity()]
        self.prefix = BirthDateColumn().label
