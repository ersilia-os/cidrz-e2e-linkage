import numpy as np
import pandas as pd
from ..preprocessing import preprocess, age, full_name, \
    birth_year, date_field, pp_utils


class RawDatasetHandler:
    def __init__(self, sourcefile):
        self.__source_file = sourcefile
        self.__field_holder = []
        self.__is_clean = False
        self.clean_columns = []
        self.__dataset = None

    def clean(self):
        if not self.__is_clean:
            self.__dataset = self.__load_raw_dataframe()

            if self.__field_holder:
                pprocess = preprocess.Preprocess(self.__dataset, self.__field_holder)
                self.clean_columns, self.__dataset = pprocess.clean()
            else:
                raise Exception('not variables were defined for cleaning')

    def set_age(self, age_column):
        self.__field_holder.append(age.Age(age_column))

    def set_fullname(self, fullname_column, other_column_names):
        self.__field_holder.append(full_name.FullName(fullname_column, other_src_cols=[other_column_names]))

    def set_birth_year(self, birth_year_column):
        self.__field_holder.append(birth_year.BirthYear(birth_year_column))

    def set_date_field(self, date_field_column):
        self.__field_holder.append(date_field.DateField(date_field_column))

    def get_dataset_field_objects(self):
        return self.__field_holder

    def get_cleaned_dataset(self):
        return self.__dataset

    def get_cleaned_column_names(self):
        return self.clean_columns

    def __load_raw_dataframe(self):
        return pd.read_csv(self.__source_file)


def test(filepath):
    sourcepath1 = filepath
    sourcepath2 = 'some path to anther file'

    source1 = RawDatasetHandler(sourcepath1)
    source1.set_age('age_birth_year')
    source1.set_birth_year('age_birth_year')
    source1.set_fullname('name', 'enrol_date')
    source1.clean()

    # source2 = RawDatasetHandler(sourcepath2)
    # source2.set_age('patient_age')
    # source2.set_fullname('patient_fullname')
    # source2.clean_dataset()

    cleaned_source1 = source1.get_cleaned_dataset()
    clean_cols_source1 = source1.get_cleaned_column_names()
    # blocks = block.get_matching_blocks(cleaned_source1, cleaned_source2)

    return cleaned_source1, clean_cols_source1  # , cleaned_source2
