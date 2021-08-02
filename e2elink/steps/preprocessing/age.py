import re
import numpy as np
from ..datautils import cleandata
from ..preprocessing import reference_field as ref


class Age(object):
    def __init__(self, src_column, output_column_prefix="clean_"):
        self.label = ref.AGE
        self.output_column_prefix = output_column_prefix
        self.source_column = src_column
        self.output_column = "{0}{1}".format(self.output_column_prefix, self.label)
        # ReferenceField.__init__(self.label, self.output_column)

    def clean(self, dataframe, range_min=0, range_max=115):
        self.df = dataframe
        self.df[self.output_column] = np.nan

        self.df[self.output_column] = self.df[self.source_column].apply(
            self.__parse_age
        )
        cleandata.sanitiseints(self.df, self.output_column, inplace=True)
        self.__age_within_range(range_min, range_max)

        return self.output_column, self.df

    def __parse_age(self, age):
        p = re.compile(r"\D")
        try:
            age = float(age)
        except:
            age = str(age)

        if isinstance(age, int) or isinstance(age, float):
            age = abs(age)

        elif isinstance(age, str):
            age = age.split(".")[0]
            age = age.lower().replace("o", "0")
            age = p.sub("", age)
        else:
            # if any(map(str.isdigit, age)):
            age = age

        return age

    def __age_within_range(self, min=0, max=115):
        for ind, row in self.df[self.df[self.output_column].notna()].iterrows():
            if min <= row[self.output_column] <= max:
                self.df.at[ind, self.output_column] = row[self.output_column]
            else:
                self.df.at[ind, self.output_column] = np.nan

    def get_label(self):
        return self.label
