import pandas as pd
import json
import os
from ... import logger

from ..setup.setup import Session
from ..schema.schema import SchemaMatch


class Preprocess(object):
    def __init__(self, src_df=None, trg_df=None):
        self.src_df = src_df
        self.trg_df = trg_df
        self.path = os.path.join(Session().get_output_path(), "preprocess")
        self.src_path = os.path.join(self.path, "src.csv")
        self.trg_path = os.path.join(self.path, "trg.csv")

    def save(self):
        self.src_df.to_csv(self.src_path, index=False)
        logger.debug("Clean source file saved to {0}".format(self.src_path))
        self.trg_df.to_csv(self.trg_path, index=False)
        logger.debug("Clean target file saved to {0}".format(self.trg_path))

    def load(self):
        logger.debug("Loading clean source file from {0}".format(self.src_path))
        src_df = pd.read_csv(self.src_path)
        logger.debug("Loading clean target file from {0}".format(self.trg_path))
        trg_df = pd.read_csv(self.trg_path)
        return Preprocess(src_df, trg_df)


# TODO: @Mwansa adapt your functions here
class _Preprocessor(object):
    def __init__(self, filename, schema):
        self.filename = os.path.abspath(filename)
        self.schema = schema
        self.df = pd.read_csv(self.filename)

    def _sort_reference_columns(self):
        logger.debug("Sorting reference columns")
        order = ["identifier", "full_name", "birth_date", "visit_date"]
        found_columns = []
        keep_columns = []
        for o in order:
            for k, v in self.schema.items():
                if o == v:
                    keep_columns += [k]
                    found_columns += [o]
        logger.debug("Keeping columns {0}".format(",".join(keep_columns)))
        rename = {}
        for k, f in zip(keep_columns, found_columns):
            rename[k] = f
        df = self.df[keep_columns]
        df = self.df.rename(columns=rename, inplace=False)
        self.df = df

    def clean(self):
        self._sort_reference_columns()
        return self.df


class Preprocessor(object):
    def __init__(self):
        self.schema = SchemaMatch().load()
        path = Session().get_output_path()
        self.src_file = os.path.join(path, "raw", "src.csv")
        self.trg_file = os.path.join(path, "raw", "trg.csv")

    def clean(self):
        logger.debug("Cleaning source file {0}".format(self.src_file))
        src_df = _Preprocessor(self.src_file, self.schema.src_match).clean()
        logger.debug("Cleaning target file {0}".format(self.trg_file))
        trg_df = _Preprocessor(self.trg_file, self.schema.trg_match).clean()
        return Preprocess(src_df, trg_df)
