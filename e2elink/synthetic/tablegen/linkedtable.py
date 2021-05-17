import numpy as np
import pandas as pd
from tqdm import tqdm


class ReferenceLinkedTables(object):
    def __init__(self, src_gen, trg_gen):
        self.src_gen = src_gen
        self.trg_gen = trg_gen

    def sample(self, src_n, trg_n, link_rate):
        src_df = self.src_gen.sample(src_n)
        src_idxs = [i for i in range(src_df.shape[0])]
        link_n = int(len(src_idxs) * link_rate)
        link_idxs = np.random.choice(src_idxs, size=link_n, replace=False)
        linked = src_df.iloc[link_idxs].reset_index(drop=True)
        trg_df = self.src_gen.sample(trg_n - linked.shape[0])
        trg_df = pd.concat([linked, trg_df], ignore_index=True)
        trg_df = trg_df.sample(frac=1).reset_index(drop=True)
        results = {"src": src_df, "trg": trg_df}
        return results


def find_ground_truth(src_uid, trg_uid):

    all_uids = list(set(src_uid).union(trg_uid))
    all_uids_idxs = {}
    for i, uid in enumerate(all_uids):
        all_uids_idxs[uid] = i

    src_uid = [all_uids_idxs[uid] for uid in src_uid]
    trg_uid = [all_uids_idxs[uid] for uid in trg_uid]

    pairs = []
    for src_idx, src_id in tqdm(enumerate(src_uid)):
        for trg_idx, trg_id in enumerate(trg_uid):
            if src_id == trg_id:
                pairs += [[src_idx, trg_idx]]
    return pd.DataFrame(pairs, columns=["src_idx", "trg_idx"])
