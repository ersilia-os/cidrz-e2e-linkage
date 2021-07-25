import pandas as pd
import json
import os
from ... import logger

from ..setup.setup import Session
from ..schema.schema import SchemaMatch
from ..preprocessing import preprocess, preprocessor, reference_field as ref

'''
get two files
get the fields that are to be cleaned
pass them to the preprocessor for the magic
retrieve the results of the dataframe
save them to your directory
and save the cleaned columns as well
'''


class E2E_Preprocessor(object):
    def __init__(self, file_to_clean, col_mapping):
        """ 2 ways to receive data to this function
        1. from the session object, in here
            a. field column map object {name: firstname, dateofbirth: dateof birth}
            b. whether a file is  src or trg file; the actual file paths
            c. directories to save the files
        2. Run independently the src and trg files, the mapping of each file
        """
        self.__preprocessor = preprocessor.Preprocessor(file_to_clean)
        self.__col_mapping = col_mapping
        self.__has_run = False

    def __set_field_column_map(self, preprocessor, col_field_mapping):
        for column, field in col_field_mapping.items():
            if field == ref.AGE:
                preprocessor.set_age(column)

            elif field == ref.BIRTH_YEAR:
                preprocessor.set_birth_year(column)

            elif field == ref.VISIT_DATE:
                preprocessor.set_date_field(column)

            elif field == ref.FULL_NAME:
                preprocessor.set_fullname(column)
            else:
                raise Exception("field not passed or unknown")

    def run(self):
        self.__set_field_column_map(self.__src_preprocessor, self.__col_mapping)
        self.__preprocessor.clean()
        self.__has_run = True

    def save(self, path=None):
        if self.__has_run:
            self.__preprocessor.get_cleaned_column_names()
            if path:
                self.__preprocessor.get_cleaned_dataset().to_csv(path)
        else:
            raise Exception("Ensure the run function has been executed before saving")

    def load(self):
        """
        return: column names, cleaned dataset
        """
        if self.__has_run:
            return self.__preprocessor.get_cleaned_column_names(), \
                   self.__preprocessor.get_cleaned_dataset()

        else:
            raise Exception("Ensure the run function has been executed before loading files")