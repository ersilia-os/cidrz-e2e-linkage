from .fullname import FullNameCompare


def get_compare(column):
    if column == "full_name":
        return FullNameCompare()
