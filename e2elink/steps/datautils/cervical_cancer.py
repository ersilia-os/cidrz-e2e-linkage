import pandas as pd
from datautils import cleandata
import numpy as np
import datetime
from datautils import data as dt

# datasource = "/Volumes/myphd_mac/Cervical cancer/MYSQL Data/leanfile.xlsx"
#datasource = "/Users/mwansa.lumpa/PhD/Datasets/Database_DATA.xlsx"

#cc = pd.read_excel(datasource)  # this is the original dataset
#c_cc = cc.copy()  # this is the copy of the dataset to be cleaned

#columnsofinterest = pd.read_csv("/Users/mwansa.lumpa/PhD/Datasets/cxca_columns_of_interest.csv")
#columnsofinterest = list(columnsofinterest['Columns'])

#columnstoclean = []

pname_cols = ['PN_NAME']
geo_location_cols = []#['CLINIC']
date_cols = ['DEDATE']
dob_cols = ['DOBDT']
age_cols = ['AGE']

cols_of_interest = pname_cols + geo_location_cols + date_cols + dob_cols + age_cols

#c_cc = c_cc[cols_of_interest]


def init_data_clean(cx_df):

    '''some general clean up
    1. remove duplicates
    2. remove data that has no names
    '''
    c_cc = cx_df
    c_cc.drop_duplicates(inplace=True)
    for pname_col in pname_cols:
        c_cc = c_cc.loc[c_cc[pname_col].notna()].copy()


    '''clean names'''
    for pname_col in pname_cols:
        c_cc = clean_full_name(c_cc, pname_col).copy()

    '''clean misc dates'''
    for date_col in date_cols:
        c_cc = cleandata.sanitisedates(c_cc, date_col).copy()

    '''clean date of birth'''
    for dob_col in dob_cols:
        c_cc = clean_cx_dob(c_cc, dob_col).copy()

    for age_col in age_cols:
        c_cc = clean_cx_age(c_cc, age_col).copy()

    return c_cc

def clean_cx_age(dataframe, colname):
    dataframe = cleandata.clean_age(dataframe, colname, 10, 100)
    return dataframe

def clean_cx_dob(dataframe, dobfield):
    '''
    DOB cleaning steps
    1. convert to date time
    2. at the end, remove dates that do not make sense - compare them with the entered ages
    3. created a new column called tmp_dob
    '''

    clean_dob_field = 'clean_dobdt'

    dataframe[clean_dob_field] = dataframe[dobfield]

    dataframe = cleandata.sanitisedates(dataframe, clean_dob_field)

    for ind, row in dataframe.loc[(dataframe[clean_dob_field].isna()) & (dataframe[dobfield].notna()), [dobfield, clean_dob_field]].iterrows():
        dataframe.at[ind, clean_dob_field] = _convert_cx_str_to_dob_date(row[dobfield])

    dataframe[clean_dob_field] = pd.to_datetime(dataframe[clean_dob_field], errors='coerce')

    return dataframe

def _convert_cx_str_to_dob_date(datetoclean):
    if datetoclean is None:
        return np.NaN

    date_to_return = np.NaN

    tmp_date = str(datetoclean).split(' ')[0] #remove the seconds part


    day_part = None
    mnth_part = None
    yr_part = None

    split_chars = ['-', '/']

    for c in split_chars:
        dateparts = tmp_date.split(c)
        if len(dateparts) > 2:
            break

    if len(dateparts) == 3:
        if len(dateparts[0]) == 4:
            yr_part = dateparts[0]
            day_part = dateparts[2]
        else:
            yr_part = dateparts[2]
            day_part = dateparts[0]

        mnth_part = dateparts[1]

    yr_part = _correct_cx_dob_year(yr_part)


    try:
        date_to_return = datetime.date(int(yr_part), int(mnth_part), int(day_part))
    except Exception as e:
        print(yr_part, mnth_part, day_part, e)
        #print(e)

    return date_to_return


def _correct_cx_dob_year(str_year):
    if len(str_year) == 4:

        lastpart = str_year[-2:]

        if 20 < int(lastpart) <= 90: #exludes all years that don't make sense
            year_part = '{0}{1}'.format(19, lastpart)#assume the last part is always correct if it less than 90
        elif int(lastpart) > 20:
            year_part = '{0}{1}{2}'.format(19, str_year[3], 5)#if the year is 0195, i convert to 1955
        else:
            return None
    else:
        return None
    return int(year_part)


#TODO refactor all this with time
def general_cleanup(c_cc_arg, pname_cols, strings_cols, date_cols, age):
    c_cc = c_cc_arg.drop_duplicates()

    # clean strings
    for strcol in strings_cols:
        c_cc = cleandata.sanitisenames(c_cc, strcol, inplace=True)

    # clean dates
    for datecol in date_cols:
        c_cc = cleandata.sanitisedates(c_cc, datecol, inplace=True)

    # clean names
    for pnamecol in pname_cols:
        c_cc = cleandata.clean_pnames(c_cc, pnamecol, inplace=True)

    # clean age
    c_cc = cleandata.clean_age(c_cc, age[0])

    return c_cc

def initial_dataset_clean(cx_dataset):
    # TODO
    '''
    1. Remove duplicates
    2. Remove empty columns
    3. Remove rows without
        a. names
        b. combination of date of birth, age and no province
    4. more cleaning needs to follow
    '''

    cx_dataset.drop_duplicates()
    return cx_dataset



# TODO
'''
Order of cleaning the data elements
1. PN_NAMES
--Split PN_NAMES into atomic names, 
--for each name, pass it through the string parser
--concatenate the names back into Surname, firstname and other names
'''

def sort_first_last_name(names):
    '''This return the firstname, last name, and all other names in that order'''
    nameorder = []
    othernames = []

    # no ambiguity here, return the names as they are
    if names is None or len(names) == 2:
        return names

    for name in names:
        #assume all names with characters are initials
        if name is None or name is np.NaN or isinstance(name, float) or len(str(name)) < 3:
            othernames.append(name)
            continue

        #the first name in the list is long and its hasn't been assigned to fname yet, so its fname
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

def clean_full_name(cx_dataset, p_name):#clean full name, rename accordingly
    '''
    Steps to clean this:
    1. sanitise the whole name using the clean function in recordlinkage library
    2. split the names into individual name tokens, clean each of the tokens using the clean function
    3. lazy sort the names to first and last name. For now, the pattern of the names are that the last
        name is always the surname, while the first one is the first name.
        The entire list of names is kept for future cleaning
    :param cx_dataset:
    :param p_name:
    :return:
    '''

    print(" in clean full names - cacx file")
    cx_dataset = cleandata.sanitisenames(cx_dataset, p_name)
    names_df = cx_dataset[p_name].str.split(' ', expand=True)


    col_names = ['pname_{0}'.format(i) for i in list(names_df)]

    names_df.columns = col_names

    titles = ['mr', 'mrs', 'miss', 'dr', 'ms']

    for colname in col_names:
        names_df = cleandata.sanitisenames(names_df, colname)

    for ind in names_df.index:
        namelist = names_df.loc[ind, col_names]
        #can probably be done in an elegant way, but gotta get this done
        #for col in col_names:
        #    val = namelist[col]
        #print('in loop:', namelist)
        for i, name in enumerate(namelist):
            if str(name).isnumeric() or name is None or name is np.nan or name.lower().strip() in titles:
                namelist[i] = np.nan
        names_df.at[ind, col_names] = sort_first_last_name(namelist)
    return cx_dataset.join(names_df)



'''
2. date of birth
3. age
4. screening date
5. province, district, facility
'''

#toclean = general_cleanup(c_cc, pname_cols, strings_cols, date_cols, age)

#primarydt = dt.data(cc, 'original cc dataset')

#primarydt.compare_summaries(toclean)

#toclean.to_excel('clean2.xlsx')
