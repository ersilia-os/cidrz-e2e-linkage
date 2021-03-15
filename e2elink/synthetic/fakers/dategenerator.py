from random import randrange
from datetime import timedelta, datetime


class DateGenerator(object):

    def __init__(self):
        pass

    def sample(self, start, end):
        start = datetime.strptime(start, '%Y-%m-%d')
        end = datetime.strptime(end, '%Y-%m-%d')
        delta = end - start
        int_delta = (delta.days * 24 * 60 * 60)
        random_second = randrange(int_delta)
        return start + timedelta(seconds=random_second)
