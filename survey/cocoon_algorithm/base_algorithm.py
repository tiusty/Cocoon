class CocoonAlgorithm(object):

    def __init__(self):
        self._homes = []
        # Need super to allow calling each classes constructor
        super(CocoonAlgorithm, self).__init__()

    @property
    def homes(self):
        return self._homes

    @homes.setter
    def homes(self, new_home):
        self._homes.append(new_home)

