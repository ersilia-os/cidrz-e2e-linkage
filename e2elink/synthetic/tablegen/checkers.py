
class NameChecker(object):

    def __init__(self, text):
        self.text = text
        self.is_empty()

    def is_empty(self):
        if str(self.text) == "nan":
            return True
        if self.text == "":
            return True
        return False

    def is_abbreviated(self):
        pass
