__author__ = "chick_0"
__version__ = "1.1.0"


# storage
class Storage(dict):
    def __init__(self):
        self.__limit__ = 0
        super().__init__()


STORAGE = Storage()
