import os
import pandas as pd
import random
import numpy as np
import names
from faker import Faker

from ... import DATA_PATH


class NameGenerator(object):

    def __init__(self):
        self.script_path = os.path.dirname(os.path.realpath(__file__))
        zam_first = pd.read_csv(os.path.join(DATA_PATH, "zambia_firstnames.tsv"), sep="\t")
        zam_last  = pd.read_csv(os.path.join(DATA_PATH, "zambia_surnames.tsv"), sep="\t")
        df_m = zam_first[zam_first["sex"] == "m"]
        df_f = zam_first[zam_first["sex"] == "f"]
        self.first_all = np.array(zam_first["name"])
        self.male = np.array(df_m["name"])
        self.female = np.array(df_f["name"])
        self.first_all_p = np.array(zam_first["prob"])
        self.male_p = np.array(df_m["prob"]) / np.sum(np.array(df_m["prob"]))
        self.female_p = np.array(df_f["prob"]) / np.sum(np.array(df_f["prob"]))
        self.last_all = np.array(zam_last["name"])
        self.last_all_p = np.array(zam_last["prob"])

    def _exp(self, sex):
        if sex is None:
            return None
        if sex == "m":
            return "male"
        if sex == "f":
            return "female"

    def first_name(self, random=False, sex=None, local=True):
        if not local:
            s = self._exp(sex)
            return names.get_first_name(gender=s).lower()
        else:
            if sex is None:
                if random:
                    return np.random.choice(self.first_all)
                else:
                    return np.random.choice(self.first_all, p=self.first_all_p)
            if sex == "m":
                if random:
                    return np.random.choice(self.male)
                else:
                    return np.random.choice(self.male, p=self.male_p)
            if sex == "f":
                if random:
                    return np.random.choice(self.female)
                else:
                    return np.random.choice(self.female, p=self.female_p)

    def last_name(self, random=False, local=True):
        if not local:
            return names.get_last_name().lower()
        else:
            if random:
                return np.random.choice(self.last_all)
            else:
                return np.random.choice(self.last_all, p=self.last_all_p)

    def full_name(self, random=False, sex=None, local=True):
        if not local:
            s = self._exp(sex)
            return names.get_full_name(gender=s).lower()
        else:
            first = self.first_name(random=random, sex=sex, local=local)
            last = self.last_name(random=random, local=local)
            full = "%s %s" % (first, last)
            return full


class NameGeneratorRough(object):

    def __init__(self):
        self.script_path = os.path.dirname(os.path.realpath(__file__))
        self.first = list(pd.read_csv(os.path.join(DATA_PATH, "first_names_moe.all.txt"), sep="\t", header=None)[0])
        self.last  = list(pd.read_csv(os.path.join(DATA_PATH, "last_names_moe.all.txt"), sep="\t", header=None)[0])

    def first_name(self):
        return np.random.choice(self.first)

    def last_name(self):
        return np.random.choice(self.last)

    def full_name(self):
        return "%s %s" % (self.first_name(), self.last_name())


class NameGeneratorDefault(object):

    def __init__(self):
        self.fake = Faker()

    def first_name(self, sex=None):
        if sex is None:
            return self.fake.first_name()
        if sex == "m":
            return self.fake.first_name_male()
        if sex == "f":
            return self.fake.first_name_female()

    def last_name(self):
        return self.fake.last_name()

    def full_name(self, sex=None):
        if sex is None:
            return self.fake.name().lower()
        if sex == "m":
            return self.fake.name_male().lower()
        if sex == "f":
            return self.fake.name_female().lower()
