import os
import numpy as np
import pandas as pd
import random
from dateutil.relativedelta import relativedelta

import hashlib
from sdv.tabular import TVAE as Model

from ..fakers.identifiergenerator import IdGeneratorDefault, ArtGenerator
from ..fakers.dategenerator import DateGenerator
from ..fakers.agegenerator import AgeGenerator
from ..fakers.namegenerator import NameGeneratorDefault, NameGenerator
from ... import MODELS_PATH

MODELS_PATH = "/Users/mduran/Desktop/test/"


class NaiveReferenceTableGenerator(object):
    def __init__(
        self,
        identifier_type=None,
        local=False,
        date_lb="2010-01-01",
        date_ub="2020-12-31",
        age_lb=10,
        age_ub=60,
        female_prop=0.5,
        duplicates_prop=0.1,
        average_visits=1.5,
    ):
        # Parameters
        self.identifier_type = identifier_type
        self.local = local
        self.date_lb = date_lb
        self.date_ub = date_ub
        self.age_lb = age_lb
        self.age_ub = age_ub
        self.female_prop = female_prop
        self.duplicates_prop = duplicates_prop
        self.average_visits = average_visits
        # Generators
        if self.identifier_type is None:
            self.identifier_generator = IdGeneratorDefault()
        else:
            self.identifier_generator = ArtGenerator()
        if self.local:
            self.name_generator = NameGenerator()
        else:
            self.name_generator = NameGeneratorDefault()
        self.date_generator = DateGenerator()
        self.age_generator = AgeGenerator()

    def _sample_identifiers(self, n):
        return [self.identifier_generator.sample() for _ in range(n)]

    def _sample_names(self, n):
        n_females = int(n * self.female_prop)
        n_males = n - n_females
        females = [self.name_generator.full_name(sex="f") for _ in range(n_females)]
        males = [self.name_generator.full_name(sex="m") for _ in range(n_males)]
        names = males + females
        sexs = ["m"] * len(males) + ["f"] * len(females)
        idxs = [i for i in range(len(names))]
        random.shuffle(idxs)
        names = [names[i] for i in idxs]
        sexs = [sexs[i] for i in idxs]
        return {"name": names, "sex": sexs}

    def _sample_dates(self, n):
        dates = [
            self.date_generator.sample(self.date_lb, self.date_ub) for _ in range(n)
        ]
        return dates

    def _sample_ages(self, n):
        loc = np.mean([self.age_lb, self.age_ub])
        scale = (self.age_ub - loc) / 1.96
        ages = [self.age_generator.sample(loc=loc, scale=scale) for _ in range(n)]
        return ages

    def _sample(self, n):
        # identifier
        identifier = self._sample_identifiers(n)
        # name
        _name = self._sample_names(n)
        full_name = _name["name"]
        sex = _name["sex"]
        # age
        _age = self._sample_ages(n)
        age = [a["years"] for a in _age]
        # visit date
        _date = self._sample_dates(n)
        visit_date = [d.strftime("%Y-%m-%d") for d in _date]
        # birth date
        birth_date = []
        for d, a in zip(_date, _age):
            bd = d - relativedelta(years=a["years"], days=a["days"])
            birth_date += [bd.strftime("%Y-%m-%d")]
        birth_year = [d.split("-")[0] for d in birth_date]

        df = pd.DataFrame(
            {
                "identifier": identifier,
                "full_name": full_name,
                "sex": sex,
                "birth_date": birth_date,
                "birth_year": birth_year,
                "age": age,
                "visit_date": visit_date,
            }
        )
        return df

    def sample(self, n):
        # exact duplicates
        prop_dupl = self.duplicates_prop
        n_dupl = int(n * prop_dupl)
        n_samp = n - n_dupl
        n_samp = max(n_samp, 1)
        if n_dupl == n:
            n_dupl -= 1
        n_samp_v = int(n_samp / self.average_visits)
        n_samp_v = max(n_samp_v, 1)
        n_vis = n_samp - n_samp_v
        df = self._sample(n_samp_v)
        idxs = [i for i in range(df.shape[0])]
        if n_vis > 0:
            df_vis = df.iloc[np.random.choice(idxs, n_vis, replace=True)]
            _date = self._sample_dates(n_vis)
            df_vis["visit_date"] = [d.strftime("%Y-%m-%d") for d in _date]
            df = pd.concat([df, df_vis])
            df = df.sample(frac=1).reset_index(drop=True)
            idxs = [i for i in range(df.shape[0])]
        if n_dupl > 0:
            df_dupl = df.iloc[np.random.choice(idxs, n_dupl, replace=True)]
            df = pd.concat([df, df_dupl])
            df = df.sample(frac=1).reset_index(drop=True)
        return df


class ReferenceTableGenerator(object):
    def __init__(self, data, model_id=None):
        self.data = data
        if model_id is None:
            self.model_id = hashlib.sha1(
                pd.util.hash_pandas_object(data).values
            ).hexdigest()
        else:
            self.model_id = model_id
        self.model_path = self._get_model_path()
        if os.path.exists(self.model_path):
            self.model = Model.load(self.model_path)

    def _get_model_path(self):
        return os.path.join(MODELS_PATH, self.model_id, "model.pkl")

    def _save(self):
        model_dir = os.path.dirname(self.model_path)
        if not os.path.exists(model_dir):
            os.mkdir(model_dir)
        self.model.save(self.model_path)

    def fit(self):
        self.model = Model(anonymize_fields={"full_name": "name"})
        self.model.fit(self.data)
        self._save()

    def sample(self, n):
        return self.model.sample(n)
