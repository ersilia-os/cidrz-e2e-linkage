import os
import pandas as pd
import random
import json

from ... import logger

from ..setup.setup import Session

MAX_N = 100


class SchemaMatch(object):
    def __init__(self, src_match=None, trg_match=None):
        self.src_match = src_match
        self.trg_match = trg_match
        self.path = os.path.join(Session().get_output_path(), "schema")
        self.src_path = os.path.join(self.path, "src.json")
        self.trg_path = os.path.join(self.path, "trg.json")

    def save(self):
        with open(self.src_path, "w") as f:
            json.dump(self.src_match, f, indent=4)
            logger.debug("Source matched schema saved to {0}".format(self.src_path))
        with open(self.trg_path, "w") as f:
            json.dump(self.trg_match, f, indent=4)
            logger.debug("Source matched schema saved to {0}".format(self.trg_path))

    def load(self):
        with open(self.src_path, "r") as f:
            src_match = json.load(f)
            logger.debug("Source matched schema loaded from {0}".format(self.src_path))
        with open(self.trg_path, "r") as f:
            trg_match = json.load(f)
            logger.debug("Target matched schema loaded from {0}".format(self.trg_path))
        return SchemaMatch(src_match, trg_match)


class ContentSampler(object):
    def __init__(self, filename):
        self.filename = os.path.abspath(filename)
        self.df = pd.read_csv(self.filename)
        self.columns = list(self.df.columns)

    def sample(self):
        content = {}
        for col in self.columns:
            vals = list(self.df[self.df[col].notnull()][col])
            if len(vals) > MAX_N:
                vals = random.sample(vals, MAX_N)
            content[col] = vals
        return content


class _SchemaMatcher(object):
    def __init__(self, filename):
        self.content = ContentSampler(filename).sample()

    def match(self):
        matching = {}
        for k, v in self.content.items():
            # dummy matching, for now
            matching[k] = k
        return matching


class SchemaMatcher(object):
    def __init__(self):
        path = Session().get_output_path()
        self.src_file = os.path.join(path, "raw", "src.csv")
        self.trg_file = os.path.join(path, "raw", "trg.csv")

    def match(self):
        logger.debug("Matching source schema")
        src_match = _SchemaMatcher(self.src_file).match()
        logger.debug("Matching target schema")
        trg_match = _SchemaMatcher(self.trg_file).match()
        logger.debug("Matching done")
        return SchemaMatch(src_match, trg_match)
