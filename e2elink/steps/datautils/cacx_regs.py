import pandas as pd
import numpy as np
from datautils import cervical_cancer as cc
from datautils import file_utils
from datautils import cleandata
import re

cols = ['name', 'enrol_date', 'age_birth_year']


def parse_age(arg):
    p = re.compile(r'\D')

    if isinstance(arg, int) or isinstance(arg, float):
        arg = abs(arg)

    if isinstance(arg, str):
        arg = arg.lower().replace('o', '0')
        return p.sub('', arg)
    else:
        return arg


def clean_age_birth_year(df, colname):
    '''
    1. sanitise the value to an integer
    2. an integer less than 115 is treated as an age,
        else it is treated as a year
    '''
    clean_col = 'c_' + colname

    df[clean_col] = df[colname]

    df[clean_col] = df[clean_col].apply(parse_age)

    # print(df[[clean_col, 'age_birth_year']].sample(20))

    df = cleandata.sanitiseints(df, clean_col)

    age_field = 'age'
    birth_year_field = 'birth_year'
    date_of_birth_field = 'dob'

    df[age_field] = np.nan
    df[birth_year_field] = np.nan

    for ind, row in df[df[clean_col].notna()].iterrows():
        if 0 < row[clean_col] < 115:
            df.at[ind, age_field] = row[clean_col]
        elif 1900 < row[clean_col] < 2020:
            df.at[ind, birth_year_field] = row[clean_col]

    return df


def clean_via_results(dataframe, colname):
    result_pos = 'pos'
    result_neg = 'neg'
    result_ind = 'indeterminate'

    tofindandreplace = {'pos': result_pos, 'neg': result_neg, 'p0s': result_pos, 'cc': result_ind, 'psitive': result_pos,'NAGATIVE': result_neg}
    dataframe = partial_match_and_replace(dataframe, colname, tofindandreplace, default_value='unknown')

    return dataframe


def partial_match_and_replace(dataframe, colname, kwargs, default_value=np.nan):
    dataframe = cleandata.sanitisestrings(dataframe, colname)
    tmpcolname = 'c_{0}'.format(colname)

    dataframe[tmpcolname] = default_value

    for key in kwargs:
        dataframe.loc[dataframe[colname].apply(lambda x: str(x).lower()).str.contains(key.lower()) == True, tmpcolname] = kwargs[key]

    return dataframe


def clean_hiv_status(dataframe, colname):
    tofindandreplace = {'pos': 'pos', 'neg': 'neg'}

    dataframe = partial_match_and_replace(dataframe, colname, tofindandreplace, default_value='unknown')

    return dataframe


def init_cacx_regs(reg_source, cols):
    reg_cacx = reg_source  # pd.read_excel(reg_source)

    # clean up screening date
    reg_cacx = clean_date_of_screening(reg_cacx, 'enrol_date').copy()

    # clean up names
    reg_cacx = clean_cacx_reg_full_name(reg_cacx, 'name').copy()

    # clean the fields that contais age, year of birth and at times date of birth
    reg_cacx = clean_age_birth_year(reg_cacx, 'age_birth_year').copy()

    reg_cacx = clean_via_results(reg_cacx, 'via').copy()

    reg_cacx = clean_hiv_status(reg_cacx, 'hivstatus').copy()

    return reg_cacx


def retrieve_trailing_names_from_date_field(df, dt_col, name_col, clean_name_col):
    for ind, row in df.loc[(df[name_col].isna() & df[dt_col].notna())].iterrows():
        # print(row[dt_col])
        # from a field like '19/20/2020 magarate mwanza', return 'margarate mwanza'
        df.at[ind, clean_name_col] = ' '.join(str(row[dt_col]).strip().split(' ')[1:])

    return df


def clean_cacx_reg_full_name(df, colname):
    clean_name = 'c_' + colname
    df[clean_name] = df[colname]

    df = retrieve_trailing_names_from_date_field(df, dt_col='enrol_date', name_col=colname, clean_name_col=clean_name)

    df = cc.clean_full_name(df, clean_name)

    return df


def clean_date_of_screening(df, colname):
    # print("in date of screening code block", colname)
    # first convert to date format
    clean_dt_col = 'clean_scr_date'
    df[clean_dt_col] = df[colname]

    df = cleandata.sanitisedates(df, clean_dt_col)

    # print(df.describe())

    for ind, row in df.loc[(df[clean_dt_col].isna() & df[colname].isna()), [colname, clean_dt_col]].iterrows():
        # print(row[colname])
        if row[colname] is None or row[colname] is np.NaN or pd.isna(row[colname]):
            continue
        df.loc[ind, clean_dt_col] = _clean_date_with_trailing_string(row[colname])

    return df


def _clean_date_with_trailing_string(dt_w_trainig_string):
    # print('this is the string:', dt_w_trainig_string)
    str_parts = dt_w_trainig_string.split(' ')
    tmp_date = np.nan
    if len(str_parts) > 0:
        tmp_date = pd.to_datetime(str_parts[0], errors='coerce')

    return tmp_date
