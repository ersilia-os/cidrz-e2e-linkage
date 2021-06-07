import numpy as np

from .identifier import IdentifierMetrics
from .full_name import FullNameMetrics
from .sex import SexMetrics
from .birth_date import BirthDateMetrics
from .visit_date import VisitDateMetrics

NULL = 0


class CompareChunk(object):
    def __init__(self, metrics):
        metrics = metrics()
        self.metrics = metrics.metrics
        self.prefix = metrics.prefix

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
        return C, columns


class CompareGetter(object):
    def __init__(self):
        pass

    @staticmethod
    def get(column):
        if column == "identifier":
            return CompareChunk(IdentifierMetrics)

        if column == "full_name":
            return CompareChunk(FullNameMetrics)

        if column == "sex":
            return CompareChunk(SexMetrics)

        if column == "birth_date":
            return CompareChunk(BirthDateMetrics)

        if column == "visit_date":
            return CompareChunk(VisitDateMetrics)

        print(column)
