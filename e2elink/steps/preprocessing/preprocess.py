import pandas as pd
import numpy as np

from ..preprocessing import (
    age,
    birth_year,
    full_name,
    alphanumeric,
    date_field,
    custom_find_replace,
    format_output,
)


class Preprocess:
    def __init__(self, dataframe, reference_field_objects):
        self.reference_fields = reference_field_objects
        self.is_cleaned = False
        self.dataframe = dataframe

    def clean(self):
        clean_output_fields = {}
        print(self.reference_fields)

        for reference_field in self.reference_fields:
            clean_col_field, self.dataframe = reference_field.clean(self.dataframe)
            clean_output_fields[reference_field.label] = clean_col_field

        self.__set_clean_dataframe(self.dataframe)
        self.is_cleaned = True
        return clean_output_fields, self.dataframe

    def __set_clean_dataframe(self, dataframe):
        self.__dataframe = dataframe

    def get_dataframe(self):
        if self.is_cleaned:
            return self.__dataframe
        else:
            self.clean()
            return self.__dataframe

    def set_clean_columns(self, columns):
        self.__clean_columns = columns

    def add_clean_columns(self, column):
        if self.__clean_columns:
            self.__clean_columns.append(column)
        else:
            self.__clean_column = [column]

    def summary(self):
        pass

    def prepare_output(self, output_format=None):
        return format_output.OutputFormat(output_format)


def preprocess_test():

    df = pd.read_csv("somefilepath")

    agefield = "age"
    cacx_age = age.Age(agefield)
    cacx_fullname = age.Age(agefield)
    cacx_birth_year = age.Age(agefield)
    cacx_screen_date = age.Age(agefield)

    cacx_reference_fields = [cacx_age, cacx_fullname, cacx_birth_year, cacx_screen_date]

    pre_process = Preprocess(df, cacx_reference_fields)

    cacx_file = pre_process.clean()

    return cacx_file
