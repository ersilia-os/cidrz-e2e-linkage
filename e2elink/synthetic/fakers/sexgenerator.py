import random


class SexGenerator(object):

    def __init__(self):
        pass

    def sample(self):
        return random.choice(["male", "female"])
