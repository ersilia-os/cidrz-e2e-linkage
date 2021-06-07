from ..metrics.metrics import LevenshteinSimilarity, TimeDaysSimilarity

from ..columns.visit_date import VisitDateColumn


class VisitDateMetrics(object):
    def __init__(self):
        self.metrics = [LevenshteinSimilarity(), TimeDaysSimilarity()]
        self.prefix = VisitDateColumn().label
