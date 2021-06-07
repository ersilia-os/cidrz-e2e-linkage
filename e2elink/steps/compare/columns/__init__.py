from .full_name import FullNameMetrics
from .birth_date import BirthDateMetrics
from .visit_date import VisitDateMetrics
from .identifier import IdentifierMetrics

NULL = 0


class Compare(object):
    def __init__(self, metrics):
        self.metrics = metrics.metrics
        self.prefix = metrics.label

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


class CompareGetter(object):
    def __init__(self):
        pass

    @staticmethod
    def get(column):
        if column == "full_name":
            return Compare(FullNameMetrics)

        if column == "birth_date":
            return Compare(BirthDateMetrics)

        if column == "visit_date":
            return Compare(VisitDateMetrics)

        if column == "identifier":
            return Compare(IdentifierMetrics)
