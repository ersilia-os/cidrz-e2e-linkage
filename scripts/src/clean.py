import os, sys
import shutil

from e2elink import MODELS_PATH


def remove(path):
    if not os.path.exists(path):
        return
    if os.path.isdir(path):
        shutil.rmtree(path)
    else:
        os.remove(path)


remove(os.path.join(MODELS_PATH, "linkage", "data"))

results_path = os.path.join(MODELS_PATH, "linkage", "results")
for tag in os.listdir(results_path):
    if len(tag) == 36:
        tag_dir = os.path.join(results_path, tag)
        remove(os.path.join(tag_dir, "raw"))
        remove(os.path.join(tag_dir, "finish"))
        remove(os.path.join(tag_dir, "evaluate"))
        remove(os.path.join(tag_dir, "schema"))
        remove(os.path.join(tag_dir, "preprocess"))
        remove(os.path.join(tag_dir, "block"))
        remove(os.path.join(tag_dir, "score", "score.npy"))
        remove(os.path.join(tag_dir, "score", "train_C.npy"))
        remove(os.path.join(tag_dir, "score", "train_columns.json"))
