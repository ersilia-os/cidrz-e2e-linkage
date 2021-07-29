import os, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.append(ROOT)
from train import Trainer

from e2elink import MODELS_PATH

data_dir = os.path.join(MODELS_PATH, "linkage", "data", "raw")

for tag in os.listdir(data_dir):
    if len(tag) == 36: # length uuid
        tr = Trainer(tag)
        tr.train()
