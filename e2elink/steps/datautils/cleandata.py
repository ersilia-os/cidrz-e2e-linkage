import pandas as pd
import numpy as np
from recordlinkage.preprocessing import clean


def sanitisestrings(dataframe, colname, inplace=True):
    if inplace:
        dataframe[colname] = clean(dataframe[colname], np.nan)
    else:
        dataframe["c_{0}".format(colname)] = clean(dataframe[colname], np.nan)

    return dataframe

#TODO refactor all this with time, add better logic and more logic
def sanitisenames(dataframe, colname, inplace=True):
    if inplace:
        dataframe[colname] = clean(dataframe[colname]).replace(r'^\s*$', np.nan, regex=True)
    else:
        dataframe["c_{0}".format(colname)] = clean(dataframe[colname], np.nan, regex=True)
    return dataframe

def sanitisedates(dataframe, colname, inplace=True):
    if inplace:
        dataframe[colname] = pd.to_datetime(dataframe[colname], errors='coerce')
    else:
        dataframe["c_{0}".format(colname)] = pd.to_datetime(dataframe[colname], errors='coerce')
    return dataframe

def sanitiseints(dataframe,colname,inplace=True):
    if inplace:
        dataframe[colname] = pd.to_numeric(dataframe[colname], errors='coerce', downcast='integer')
    else:
        dataframe["c_{0}".format(colname)] = pd.to_numeric(dataframe[colname], errors='coerce')
    return dataframe

def clean_age(dataframe,colname, lowerbound=10, upperbound=105, inplace=True):
    dataframe = sanitiseints(dataframe, colname)
    if inplace:
        dataframe.loc[(dataframe[colname] < lowerbound) | dataframe[colname] > upperbound, colname] = np.nan
    else:
        pass
    return dataframe

def clean_pnames(dataframe, colname, inplace=True):
    # drop hanging characters, join names that make sense
    dataframe = sanitisenames(dataframe, colname)
    dataframe[colname] = \
        dataframe[colname].apply(lambda unnames: ' '.join([name for name in str(unnames).split() if len(name) > 2]).strip())

    dataframe.loc[dataframe[colname].str.len() < 3] = np.nan
    return dataframe
