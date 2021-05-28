from fuzzywuzzy import fuzz
import textdistance
import py_stringmatching as str_match


class ExactSimilarity(object):
    def __init__(self):
        self.label = "ex"

    def calculate(self, a, b):
        if a == b:
            return 1.
        else:
            return 0.


class LevenshteinSimilarity(object):
    def __init__(self):
        self.label = "lev"

    def calculate(self, a, b):
        return fuzz.ratio(a, b) / 100.0


class JaroWinklerSimilarity(object):
    def __init__(self):
        self.label = "jw"

    def calculate(self, a, b):
        return textdistance.jaro_winkler.normalized_similarity(a, b)


class MatchRatingApproach(object):
    def __init__(self):
        self.label = "mra"

    def calculate(self, a, b):
        return textdistance.mra(a, b)


class CosineSimilarity(object):
    def __init__(self):
        self.label = "cos"

    def calculate(self, a, b):
        return textdistance.cosine.normalized_similarity(a, b)


class MongeElkanLevenshteinSimilarity(object):
    def __init__(self):
        self.label = "melev"
        self.me = str_match.MongeElkan()
        self.me.set_sim_function(str_match.Levenshtein().get_raw_score)

    def calculate(self, a, b):
        return self.me.get_raw_score(a.split(" "), b.split(" "))


class MongeElkanJaroWinklerSimilarity(object):
    def __init__(self):
        self.label = "mejw"
        self.me = str_match.MongeElkan()
        self.me.set_sim_function(str_match.JaroWinkler().get_raw_score)

    def calculate(self, a, b):
        return self.me.get_raw_score(a.split(" "), b.split(" "))
