from ..preprocessing import reference_field as ref, age


class BirthYear(age.Age):
    def __init__(self, src_column, output_column_prefix="clean_"):
        age.Age.__init__(self, src_column, output_column_prefix)
        self.label = ref.BIRTH_YEAR
        self.output_column = "{0}{1}".format(self.output_column_prefix, self.label)

    def clean(self, dataframe):
        return age.Age.clean(self, dataframe, 1900, 2021)
