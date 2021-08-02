import numpy as np


def merge_columns(dataframe, final_col_name, cols_to_merge=[], separator=" "):
    dataframe[final_col_name] = np.nan

    # TODO -fix middlename that has nan, actually names that have nan
    for id, columns in dataframe.iterrows():
        tmpfullname = ""
        separator_char = ""
        for col in cols_to_merge:
            if columns[col] is np.nan or columns[col] is None:
                continue
            tmpfullname += "{0}{1}".format(separator_char, columns[col])
            separator_char = separator

        dataframe.at[id, final_col_name] = tmpfullname

    return dataframe
