import os
import numpy as np
import fasttext
from scipy.spatial.distance import euclidean, cosine
import random
from tqdm import tqdm

from .. import DATA_PATH, MODELS_PATH
from ..synthetic.fakers.namegenerator import NameGeneratorRough
from ..synthetic.fakers.namegenerator import NameGenerator
from ..synthetic.misspell.simple import SimpleMisspell
from ..synthetic.misspell.moe import MoeMisspell
from ..synthetic.misspell.zambia import ZambiaMisspell


EMB_DIM = 128


class NameGenericVectorizer(object):
    def __init__(self):
        self.emb_dim = EMB_DIM
        self.script_path = os.path.dirname(os.path.realpath(__file__))
        self.data_path = os.path.join(DATA_PATH, "names_with_misspells.txt")
        self.model_path = os.path.join(MODELS_PATH, "name_generic-%d.bin" % EMB_DIM)
        if os.path.exists(self.model_path):
            self.mod = fasttext.load_model(self.model_path)

    def _prepare_data(self, N=100000, n=5):
        ngr = NameGeneratorRough()
        ng = NameGenerator()
        sm = SimpleMisspell()
        ms = MoeMisspell()
        zm = ZambiaMisspell()
        with open(self.data_path, "w", encoding="utf-8") as f:
            done = set()
            for _ in tqdm(range(0, N)):
                x = []
                x += [ng.first_name(random=True)]
                x += [ng.first_name(random=False)]
                x += [ng.last_name(random=True)]
                x += [ng.last_name(random=False)]
                x += [ng.first_name(random=True, local=False)]
                x += [ng.first_name(random=False, local=False)]
                x += [ng.last_name(random=True, local=False)]
                x += [ng.last_name(random=False, local=False)]
                x += [ngr.first_name()]
                x += [ngr.last_name()]
                for x_ in x:
                    if x_ in done:
                        continue
                    a_zm = zm.misspell(x_, n=n)
                    l_ms = ms.misspell(x_, n=n, sort=True)
                    r_ms = ms.misspell(x_, n=n, sort=False)
                    if l_ms is None:
                        l_ms = sm.misspell(x_, n=n)
                    if r_ms is None:
                        r_ms = sm.misspell(x_, n=n)
                    a_ms = l_ms + r_ms
                    random.shuffle(a_ms)
                    if a_zm is None:
                        a = a_ms[: len(l_ms)] + [x_] + a_ms[len(l_ms) :]
                    else:
                        a = a_ms[: len(l_ms)] + [x_] + a_zm + a_ms[len(l_ms) :]
                    f.write("%s\n" % " ".join(a))
                done.update(x)
                if len(done) > N:
                    break

    def fit(self, epoch=30):
        mod = fasttext.train_unsupervised(
            self.data_path, dim=self.emb_dim, min_count=1, epoch=epoch
        )
        print("Words:", len(mod.words))
        print("Dim  :", mod.dim)
        print("Epoch:", mod.epoch)
        mod.save_model(self.model_path)
        self.mod = mod

    def vectorize(self, words):
        V = np.zeros((len(words), self.emb_dim))
        for i, word in enumerate(words):
            V[i, :] = self.mod.get_sentence_vector(word)
        return V

    def compare(self, word1, word2, metric="euclidean"):
        words = [word1, word2]
        V = self.vectorize(words)
        if metric == "euclidean":
            metric = euclidean
        if metric == "cosine":
            metric = cosine
        return metric(V[0], V[1])

    def similarity(self, word1, word2, metric="euclidean", cap=False):
        sim = 1 - self.compare(word1, word2, metric=metric)
        if cap:
            return max(sim, 0)
        else:
            return sim
