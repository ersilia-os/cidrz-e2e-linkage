import pandas as pd
import numpy as np
import os
import uuid

from ... import DATA_PATH


class IdGeneratorDefault(object):
    def __init__(self):
        pass

    def sample(self):
        return str(uuid.uuid4())[:13]


class ArtGenerator(object):
    def __init__(self):
        self.script_path = self.script_path = os.path.dirname(
            os.path.realpath(__file__)
        )
        self.arts = list(
            pd.read_csv(os.path.join(DATA_PATH, "art_lims.tsv"), sep="\t", header=None)[
                0
            ]
        )

    def sample(self):
        return np.random.choice(self.arts)
