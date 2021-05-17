import numpy as np
import random


class AgeGenerator(object):
    def __init__(self):
        pass

    def sample(self, loc, scale):
        years = int(np.random.normal(loc=loc, scale=scale))
        years = np.clip(years, 0, 120)
        days = random.randint(0, 365)
        return {"years": years, "days": days}
