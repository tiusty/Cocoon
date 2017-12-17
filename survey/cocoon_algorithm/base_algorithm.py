class CocoonAlgorithm(object):

    def __init__(self):
        self._homes = []

    @property
    def homes(self):
        return self._homes

    @homes.setter
    def homes(self, new_home):
        self._homes.append(new_home)

