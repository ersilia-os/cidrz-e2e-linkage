from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import pandas as pd
import numpy as np

import faiss


class Block:
    def __init__(self, dimension, custom_index=None):
        self.is_custom_index = custom_index is not None
        if not self.is_custom_index:
            self.index = faiss.IndexFlatL2(dimension)
        else:
            self.index = custom_index

    def add_with_ids(self, data, ids):
        if not self.is_custom_index:
            self.index = faiss.IndexIDMap(self.index)
        self.index.add_with_ids(data, ids)

    def add(self, data):
        self.index.add(data)

    def create_blocks(self, block_query, k=30):
        distance_, blocks_ = self.index.search(block_query, k)
        return blocks_


class Vectoriser:
    def __init__(self, vectoriser=None):
        self.is_fitted = False
        if vectoriser is None:
            self._vectoriser = TfidfVectorizer(
                analyzer="char_wb", ngram_range=(2, 2), max_features=200
            )
        else:
            self._vectoriser = vectoriser

    def fit(self, data):
        self.is_fitted = True
        return self._vectoriser.fit(data)

    def transform(self, data):
        matrix = None
        if self.is_fitted:
            matrix = self._vectoriser.transform(data)
        return matrix

    def get_feature_names(self):
        feature_names = ""
        if self.is_fitted:
            feature_names = self._vectoriser.get_feature_names()
        return feature_names

    def get_vectoriser(self):
        return self._vectoriser


def get_matching_blocks(query, query_field, target, target_field):
    vect = Vectoriser()

    vect.fit(target[target_field])
    target_matrix = vect.transform(target[target_field])

    query_matrix = vect.transform(query[query_field])

    block = Block(target_matrix.shape[1])

    block.add_with_ids(
        target_matrix.toarray().astype("float32"), np.array(target.index)
    )
    blocks = block.create_blocks(query_matrix.toarray().astype("float32"))

    return blocks


def test():

    ca_df = pd.read_csv(
        "/Users/mwansa.lumpa/PhD/Datasets/SmartCare/toshare/final_to_share/ca_original_clean.csv"
    )
    sc_df = pd.read_csv(
        "/Users/mwansa.lumpa/PhD/Datasets/SmartCare/toshare/final_to_share/sc_original_clean.csv"
    )

    ca_to_match = pd.DataFrame()
    sc_to_match = pd.DataFrame()

    ca_to_match["vector_field"] = (
        ca_df.loc[(ca_df["c_name"].notna()) & (ca_df["birth_year_coalesce"].notna())][
            "c_name"
        ]
        + " "
        + ca_df.loc[(ca_df["c_name"].notna()) & (ca_df["birth_year_coalesce"].notna())][
            "birth_year_coalesce"
        ]
        .astype("int32")
        .astype(str)
    )

    sc_to_match["vector_field"] = (
        sc_df.loc[(sc_df["full_name"].notna()) & (sc_df["birth_year"].notna())][
            "full_name"
        ]
        + " "
        + sc_df.loc[(sc_df["full_name"].notna()) & (sc_df["birth_year"].notna())][
            "birth_year"
        ]
        .astype("int32")
        .astype(str)
    )

    blocks = get_matching_blocks(
        ca_to_match, "vector_field", sc_to_match, "vector_field"
    )

    """
    for query_id, result_block in zip(ca_to_match.index, blocks):
        print('Query ID, and Query - {0} {1}'.format(query_id, ca_df.loc[query_id]))
        for result_id in result_block:
            print('---------------------------')
            print('{0} {1} {2}'.format(result_id, sc_to_match.loc[result_id], sc_df.loc[result_id]['Facility']))
            #print('---------------------------')
        print('##################################################################')
        value = input('Press any key to continue or 1 to quit')
        if value == str(1):
            exit()
    """

    return (
        ca_to_match.index,
        ca_df,
        blocks,
        sc_df,
    )  # TODO for the ca_df, filter only to those that had matches
