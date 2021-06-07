from ....metrics.metrics import FirstCharacterSimilarity

from ....columns.sex import SexColumn


class SexMetrics(object):
    def __init__(self):
        self.metrics = [FirstCharacterSimilarity()]
        self.prefix = SexColumn().label
