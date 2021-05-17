from .columns import get_compare


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
        pass

    def compare(self, pairs, src, trg):
        comp = get_compare(column)


        return Comparison(pairs, C, columns)
