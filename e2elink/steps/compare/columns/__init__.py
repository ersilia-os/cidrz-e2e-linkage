from .fullname import FullNameCompare
from .birthdate import BirthDateCompare


class CompareGetter(object):

    def __init__(self):
        pass

    @staticmethod
    def get(column):
        if column == "full_name":
            return FullNameCompare()

        if column == "birth_date":
            return BirthDateCompare()

        if column == "visit_date":
            return VisitDateCompare()

        if column == "identifier":
            return IdentifierCompare()
