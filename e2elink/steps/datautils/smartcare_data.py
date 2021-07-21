from datautils import cleandata
import pandas as pd
import numpy as np

'''colums of interes
    geography: facility, province, district
    identification: patientguid, firstname, last name, middlename
    other bio: date of birth, sex
    clinical info: art start date, ihap date
        
'''

def init_sc_data(dataframe):

    dataframe = get_full_name(dataframe, firstname='FirstName', surname='SurName', middlename='MiddleName').copy()
    dataframe = cleandata.sanitisedates(dataframe, 'DateOfBirth', False).copy()
    dataframe = year_part(dataframe, 'DateOfBirth').copy()

    return dataframe

def year_part(dataframe, datecolumn):
    dataframe['birth_year'] = dataframe[datecolumn].dt.year

    return dataframe

def get_full_name(dataframe, firstname=None, surname=None, middlename=None):
    fullname = 'full_name'
    firstname = 'FirstName'
    lastname = 'SurName'
    middlename = 'MiddleName'

    dataframe[fullname] = ''

    cleandata.sanitisenames(dataframe, firstname)
    cleandata.sanitisenames(dataframe, middlename)
    cleandata.sanitisenames(dataframe, lastname)

    #TODO -fix middlename that has nan, actually names that have nan:w
    orderofnames = ['FirstName', 'MiddleName', 'SurName']
    for id, names in dataframe.iterrows():
        tmpfullname = ''
        delimeter_char = ''
        for name in orderofnames:
            if names[name] is np.nan or names[name] is None:
                continue
            tmpfullname += "{0}{1}".format(delimeter_char, names[name])
            delimeter_char = ' '

        dataframe.at[id, fullname] = tmpfullname

    return dataframe




