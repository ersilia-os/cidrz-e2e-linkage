import numpy as np
import pandas as pd

from ..schema.default import ColumnSynonym
from ..misspell.simple import SimpleMisspell


class TableTransformer(object):

    def __init__(self, ref_data):
        self.ref_data = ref_data
        self.data = ref_data.copy()
        self.data["visit_date_dt"] = pd.to_datetime(self.data["visit_date"])
        self.data["birth_date_dt"] = pd.to_datetime(self.data["birth_date"])

    def _select_idxs(self, rate):
        n = self.data.shape[0]
        f = int(n*rate)
        idxs = [i for i in range(n)]
        return np.random.choice(idxs, f, replace=False)

    def _column_as_list(self, column):
        return list(self.data[column])

    def _abbreviate_full_name(self, rate):
        idxs = self._select_idxs(rate)
        names = self._column_as_list("full_name")
        for i in idxs:
            name = names[i].split(" ")
            name = " ".join([name[0][0]] + name[1:])
            names[i] = name
        self.data["full_name"] = names

    def _age_coverage(self, cov):
        idxs = self._select_idxs(1-cov)
        col = self._age_format
        age_data = self._column_as_list(col)
        for i in idxs:
            age_data[i] = np.nan
        self.data[col] = age_data

    def _choose_age_format(self, format):
        age_cols = ["birth_date", "birth_year", "age"]
        rm_cols = [a for a in age_cols if a != format]
        self._age_format = format
        self.data = self.data.drop(columns=rm_cols)

    def _date_format(self, format):
        if format != "%Y-%m-%d":
            self.data["visit_date"] = self.data["visit_date_dt"].dt.strftime(format)
            self.data["birth_date"] = self.data["birth_date_dt"].dt.strftime(format)

    def _date_coverage(self, cov):
        idxs = self._select_idxs(1-cov)
        col = "visit_date"
        dates = self._column_as_list(col)
        for i in idxs:
            dates[i] = np.nan
        self.data[col] = dates

    def _full_name_format(self, format):
        names = self._column_as_list("full_name")
        if format == "title":
            names = [n.title() for n in names]
        elif format == "lower":
            names = [n.lower() for n in names]
        elif format == "upper":
            names = [n.upper() for n in names]
        else:
            pass
        self.data["full_name"] = names

    def _full_name_coverage(self, cov):
        idxs = self._select_idxs(1-cov)
        if "full_name" in list(self.data.columns):
            names = self._column_as_list("full_name")
            for i in idxs:
                names[i] = np.nan
            self.data["full_name"] = names
        else:
            fnames = self._column_as_list("first_name")
            lnames = self._column_as_list("last_name")
            for i in idxs:
                fnames[i] = np.nan
                lnames[i] = np.nan
            self.data["first_name"] = fnames
            self.data["last_name"] = lnames

    def _hide_identifier(self):
        self.data = self.data.drop(columns="identifier")

    def _identifier_coverage(self, cov):
        idxs = self._select_idxs(1-cov)
        col = "identifier"
        ids = self._column_as_list(col)
        for i in idxs:
            ids[i] = np.nan
        self.data[col] = ids

    def _misspell_full_name(self, rate):
        ms = SimpleMisspell()
        idxs = self._select_idxs(rate)
        names = self._column_as_list("full_name")
        js = np.random.choice([0, 1], len(idxs), replace=True)
        for i,j in zip(idxs, js):
            name = names[i].split(" ")
            if len(name) == 0:
                j = 0
            ms_ = ms.misspell(name[j], n=1)[0]
            if ms_:
                name[j] = ms_
            names[i] = " ".join(name)
        self.data["full_name"] = names

    def _rename_columns(self):
        cs = ColumnSynonym()
        cap_type = cs.style()
        new_cols = {}
        for col in list(self.data.columns):
            new_cols[col] = cs.rename(col, cap_type=cap_type)
        self.data = self.data.rename(columns=new_cols)

    def _sex_format(self, format):
        if format != "lower_abbrv":
            sexs = self._column_as_list("sex")
            if format == "upper_abbrv":
                sexs = [s.upper() for s in sexs]
            if format == "lower":
                sexs_ = []
                for s in sexs:
                    if s[0] == "m":
                        sexs_ += ["male"]
                    else:
                        sexs_ += ["female"]
                sexs = sexs_
            if format == "title":
                sexs_ = []
                for s in sexs:
                    if s[0] == "m":
                        sexs_ += ["Male"]
                    else:
                        sexs_ += ["Female"]
                sexs = sexs_
            self.data["sex"] = sexs

    def _shuffle_columns(self):
        columns = list(self.data.columns)
        columns.shuffle()
        self.data = self.data[columns]

    def _sort_by_date(self):
        self.data = self.data.sort_values(by="visit_date_dt").reset_index(drop=True)

    def _split_full_name(self):
        names = self._column_as_list("full_name")
        first_names = []
        last_names = []
        for name in names:
            name = name.split(" ")
            if len(name) == 1:
                first_names += [np.nan]
                last_names += name
            else:
                first_names += [name[0]]
                last_names += [" ".join(name[1:])]
        columns = list(self.data.columns)
        idx = columns.index("full_name")
        if idx == 0:
            columns = ["first_name", "last_name"] + columns[1:]
        else:
            columns = columns[:idx] + ["first_name", "last_name"] + columns[(idx+1):]
        self.data["first_name"] = first_names
        self.data["last_name"] = last_names
        self.data = self.data[columns]

    def _swap_full_name(self, rate):
        idxs = self._select_idxs(rate)
        names = self._column_as_list("full_name")
        for i in idxs:
            name = names[i].split(" ")
            name.reverse()
            names[i] = " ".join(name)
        self.data["full_name"] = names

    def transform(self, params):

        if "sort_by_date" in params:
            if params["sort_by_date"]:
                self._sort_by_date()

        if "age_format" in params:
            self._choose_age_format(params["age_format"])

        if "date_format" in params:
            self._date_format(params["date_format"])

        if "age_coverage" in params:
            self._age_coverage(params["age_coverage"])

        if "date_coverage" in params:
            self._date_coverage(params["date_coverage"])

        if "identifier_coverage" in params:
            self._identifier_coverage(params["identifier_coverage"])

        if "hide_identifier" in params:
            if params["hide_identifier"]:
                self._hide_identifier()

        if "misspell_full_name" in params:
            self._misspell_full_name(params["misspell_full_name"])

        if "swap_full_name" in params:
            self._swap_full_name(params["swap_full_name"])

        if "abbreviate_full_name" in params:
            self._abbreviate_full_name(params["abbreviate_full_name"])

        if "name_format" in params:
            self._full_name_format(params["name_format"])

        if "sex_format" in params:
            self._sex_format(params["sex_format"])

        if "shuffle_columns" in params:
            if params["shuffle_columns"]:
                self._shuffle_columns()

        if "split_full_name" in params:
            if params["split_full_name"]:
                self._split_full_name()

        if "name_coverage" in params:
            self._full_name_coverage(params["name_coverage"])

        self.data = self.data.drop(columns=["visit_date_dt", "birth_date_dt"])
        self.data.fillna("", inplace=True)

        if "rename_columns" in params:
            self._rename_columns()

    def reset(self):
        return TableTransformer(self.ref_data.copy())
