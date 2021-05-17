import random
from ...vectorize.namegeneric import NameGenericVectorizer


class EmbeddingMisspell(object):
    def __init__(self):
        self.ngv = NameGenericVectorizer()

    def misspell(self, word, n, rand=False, max_neigh=10):
        if not rand:
            nn = self.ngv.mod.get_nearest_neighbors(word, n)
            return [x[1] for x in nn]
        else:
            nn = self.ngv.mod.get_nearest_neighbors(word, max_neigh)
            return random.sample([x[1] for x in nn], min(n, len(nn)))
