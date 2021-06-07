from ..metrics.metrics import ExactSimilarity

from ..columns.identifier import IdentifierColumn


class IdentifierMetrics(object):
    def __init__(self):
        self.metrics = [ExactSimilarity()]
        self.prefix = IdentifierColumn().label
