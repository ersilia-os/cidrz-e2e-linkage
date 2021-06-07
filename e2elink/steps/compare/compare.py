from .columns import CompareGetter


class Comparison(object):
    def __init__(self, pairs, C, columns):
        self.pairs = pairs
        self.C = C
        self.columns = columns

    def save(self):
        pass

    def load(self):
        pass


class Compare(object):
    def __init__(self):
        self._compare_getter = CompareGetter()

    def _get_comparisons_columns(self):
        pass

    def compare(self, pairs, src, trg):

        comp = self._compare_getter.get(column)

        return Comparison(pairs, C, columns)
