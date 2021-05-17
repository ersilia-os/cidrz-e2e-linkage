import os
import random
import re
import numpy as np


class ArtNumber(object):
    def __init__(self, art, clean=True):
        art = str(art)
        if clean:
            art = re.sub("-.-", "", art)
            art = art.replace("/", "-")
            art = art.replace(" ", "-")
        self.art = art

    def __str__(self):
        return str(self.art)

    def is_valid(self):
        if str(self.art) == "nan":
            return False
        art = self.art.split("-")
        if len(art) != 4:
            return False
        a, b, c, d = art
        if len(a) < 4:
            return False
        a = a[-4:]
        if len(b) != 3:
            return False
        if len(d) != 1:
            return False
        try:
            d = int(d)
        except:
            return False
        if len(c) != 5:
            return False
        try:
            s = np.sum([int(x) for x in c])
        except:
            return False
        s = "%d" % s
        s = int(s[-1])
        if s != d:
            return False
        return True

    def has_checkdigit(self):
        if self.art[-2] != "-":
            return False
        else:
            return True

    def get_code(self):
        if self.art[-2] != "-":
            return np.nan
        code = self.art.split("-")[-2][-5:].zfill(5)
        return code

    def get_district(self):
        dis = self.art.split("-")[0][-4:].zfill(4)
        return dis

    def get_facility(self):
        try:
            fac = self.art.split("-")[1][-3:].zfill(3)
            return fac
        except:
            return np.nan

    def get_checkdigit(self):
        dig = self.art.split("-")[-1]
        return dig

    def calc_checkdigit(self):
        try:
            cod = self.get_code()
            s = 0
            for x in cod:
                s += int(x)
            dig = "%d" % s
            return dig[-1]
        except:
            return np.nan

    def checkdigit(self):
        try:
            a = self.calc_checkdigit()
            b = self.get_checkdigit()
            if a == b:
                return True
            else:
                return False
        except:
            return False

    def sanitize(self):
        cod = self.get_code()
        fac = self.get_facility()
        dis = self.get_district()
        dig = self.calc_checkdigit()
        if (
            str(cod) == "nan"
            or str(fac) == "nan"
            or str(dis) == "nan"
            or str(dig) == "nan"
        ):
            return np.nan
        else:
            return dis + "-" + fac + "-" + cod + "-" + dig
