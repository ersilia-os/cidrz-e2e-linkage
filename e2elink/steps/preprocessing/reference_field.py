import numpy as np
import pandas as pd

AGE = "age"
BIRTH_YEAR = "birth_year"
FULL_NAME = "full_name"
VISIT_DATE = "screening_date"
DATE_OF_BIRTH = "date_of_birth"
STRING_FIELD = "string_field"
INT_FIELD = "integer_field"


class ReferenceField:
    def __init__(self, field_label, column, output_column_prefix="clean_"):
        self.label = field_label
        self.output_column_prefix = output_column_prefix
        self.source_column = column
        self.output_column = "{0}{1}".format(self.output_column_prefix, column)

    def clean(self, dataframe):
        return np.nan, dataframe

    def get_label(self):
        return self.label

    def get_column_prefix(self):
        return self.output_column_prefix

    def get_source_column(self):
        return self.source_column

    def get_output_columns(self):
        return self.output_column
