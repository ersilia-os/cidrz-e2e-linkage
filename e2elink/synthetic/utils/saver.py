import json
import os
import shutil


def save_results(
    root, name, src_df, trg_df, truth_df, src_params, trg_params, truth_params
):
    path = os.path.join(root, name)
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)
    src_df.to_csv(os.path.join(path, "source.csv"), index=False)
    trg_df.to_csv(os.path.join(path, "target.csv"), index=False)
    truth_df.to_csv(os.path.join(path, "truth.csv"), index=False)
    del src_params["misspeller"]
    del trg_params["misspeller"]
    params = {"source": src_params, "target": trg_params, "truth": truth_params}
    with open(os.path.join(path, "params.json"), "w") as f:
        json.dump(params, f, indent=4)
