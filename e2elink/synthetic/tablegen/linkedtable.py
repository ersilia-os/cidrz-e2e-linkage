import numpy as np
import pandas as pd


class ReferenceLinkedTables(object):

    def __init__(self, src_gen, trg_gen):
        self.src_gen = src_gen
        self.trg_gen = trg_gen

    def sample(self, src_n, trg_n, link_rate):
        src_df = self.src_gen.sample(src_n)
        src_idxs = [i for i in range(src_df.shape[0])]
        link_n = int(len(src_idxs)*link_rate)
        link_idxs = np.random.choice(src_idxs, size=link_n, replace=False)
        linked = src_df.iloc[link_idxs].reset_index(drop=True)
        linked["src_idx"] = link_idxs
        trg_df = self.src_gen.sample(trg_n - linked.shape[0])
        trg_df["src_idx"] = np.nan
        trg_df = pd.concat([linked, trg_df], ignore_index=True)
        trg_df = trg_df.sample(frac=1).reset_index(drop=True)
        pdf = trg_df[trg_df["src_idx"].notnull()].sample(frac=1).reset_index(drop=False)
        pairs_df = pd.DataFrame(
            {"src_idx": np.array(pdf["src_idx"]).astype(np.int),
             "trg_idx": pdf["index"]}
        )
        results = {
            "src": src_df,
            "trg": trg_df.drop(columns="src_idx"),
            "pairs": pairs_df
        }
        return results
