import numpy as np
from ..datautils import cleandata
from ..preprocessing import reference_field as ref


class FullName:
    def __init__(self, src_column, output_column_prefix="clean_", other_src_cols=None):
        self.label = ref.FULL_NAME
        self.output_column_prefix = output_column_prefix
        self.source_column = src_column
        self.output_column = "{0}{1}".format(self.output_column_prefix, self.label)
        self.other_source_columns = other_src_cols

    def clean(self, dataframe):
        self.df = dataframe
        self.df[self.output_column] = self.df[self.source_column]

        if self.other_source_columns:
            for col in self.other_source_columns:
                self.__retrieve_training_name_from_other_col(col)

        self.df = cleandata.sanitisenames(self.df, self.output_column)
        other_clean_cols, self.df = self.__get_name_tokens_sorted()
        # self.__other_cleaned_columns(other_clean_cols)
        return self.output_column, self.df

    def __other_cleaned_columns(self, other_columns):
        self.output_column = other_columns

    def __retrieve_training_name_from_other_col(self, column_name):
        for ind, row in self.df.loc[
            (self.df[self.source_column].isna() & self.df[column_name].notna())
        ].iterrows():
            # print(row[dt_col])
            # from a field like '19/20/2020 magarate mwanza', return 'margarate mwanza'
            self.df.at[ind, self.output_column] = " ".join(
                str(row[column_name]).strip().split(" ")[1:]
            )

    def __get_name_tokens_sorted(self):
        names_df = self.df[self.output_column].str.split(" ", expand=True)
        col_names = ["{0}_{1}".format(self.output_column, i) for i in list(names_df)]

        names_df.columns = col_names

        titles = ["mr", "mrs", "miss", "dr", "ms"]

        for colname in col_names:
            names_df = cleandata.sanitisenames(names_df, colname)

        for ind in names_df.index:
            namelist = names_df.loc[ind, col_names]
            # can probably be done in an elegant way, but gotta get this done
            # for col in col_names:
            #    val = namelist[col]
            # print('in loop:', namelist)
            for i, name in enumerate(namelist):
                if (
                    str(name).isnumeric()
                    or name is None
                    or name is np.nan
                    or name.lower().strip() in titles
                ):
                    namelist[i] = np.nan
            names_df.at[ind, col_names] = self.sort_first_last_name(namelist)
        return col_names, self.df.join(names_df)

    def sort_first_last_name(self, names):
        """This return the firstname, last name, and all other names in that order"""
        nameorder = []
        othernames = []

        # no ambiguity here, return the names as they are
        if names is None or len(names) == 2:
            return names

        for name in names:
            # assume all names with characters are initials
            if (
                name is None
                or name is np.NaN
                or isinstance(name, float)
                or len(str(name)) < 3
            ):
                othernames.append(name)
                continue

            # the first name in the list is long and its hasn't been assigned to fname yet, so its fname
            if len(nameorder) == 0 and len(str(name)) > 2:
                nameorder.append(name)

            elif len(nameorder) > 0:
                if len(str(name)) < 3:
                    othernames.append(name)
                elif len(nameorder) == 1:
                    nameorder.append(name)
                else:
                    othernames.append(nameorder[1])
                    nameorder[1] = name

        return nameorder + othernames
