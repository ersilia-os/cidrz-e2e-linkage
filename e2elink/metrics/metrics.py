from fuzzywuzzy import fuzz
import textdistance


class LevenshteinSimilarity(object):
    def __init__(self):
        self.label = "lev"

    def calculate(self, a, b):
        return fuzz.ratio(a, b) / 100.0


class JaroWinklerSimilarity(object):
    def __init__(self):
        self.label = "jw"

    def calculate(self, a, b):
        return textdistance.jaro_winkler(a, b)


class MatchRatingApproach(object):
    def __init__(self):
        self.label = "mra"

    def calculate(self, a, b):
        return textdistance.mra(a, b)
