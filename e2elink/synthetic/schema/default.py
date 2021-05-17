import random


COLUMN_SYNONYMS = {
    "identifier": [
        "client id",
        "number",
        "unique id"
    ],
    "full_name": [
        "name",
        "full name",
        "client name",
        "client"
    ],
    "first_name": [
        "first name",
        "given name",
    ],
    "last_name": [
        "family name",
        "surname",
        "last name"
    ],
    "sex": [
        "gender"
    ],
    "birth_date": [
        "date of birth",
        "birthdate",
    ],
    "birth_year": [
        "year of birth",
        "birthyear"
    ],
    "age": [

    ],
    "visit_date": [
        "visit date",
        "date of visit",
        "date"
    ],
    "entry_date": [
        "entry date",
        "date of entry"
    ],
    "clinical_variable": [
        "hiv",
        "via",
        "hiv status",
        "via status"
    ]
}


class ColumnSynonym(object):

    def __init__(self):
        self.ref2syn = dict((k, [k] + v) for k,v in COLUMN_SYNONYMS.items())
        self.cap_styles = ["lower", "upper", "capitalize", "title"]

    def style(self):
        return random.choice(self.cap_styles)

    def rename(self, ref_col, cap_type=None, syn_option=None):
        syn = self.ref2syn[ref_col]
        if syn_option is None:
            col = random.choice(self.ref2syn[ref_col])
        else:
            i = min(len(syn)-1, syn_option)
            col = syn[i]
        if cap_type is None:
            cap_type = random.choice([0, 1, 2])
        else:
            if type(cap_type) is not int:
                cap_type = self.cap_styles.index(cap_type)
        if cap_type == 0:
            col = col.lower()
        elif cap_type == 1:
            col = col.upper()
        elif cap_type == 2:
            col = col.capitalize()
        else:
            col = col.title()
        return col
