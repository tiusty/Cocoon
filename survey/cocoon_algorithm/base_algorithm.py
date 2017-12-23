class CocoonAlgorithm(object):

    def __init__(self):
        self._homes = []
        self._destinations = []
        # Need super to allow calling each classes constructor
        super(CocoonAlgorithm, self).__init__()

    @property
    def homes(self):
        """
        Get the list of homes stored
        :return: A list of homes
        """
        return self._homes

    @homes.setter
    def homes(self, new_home):
        """
        Add home to homes list.
        If the variable is a list, then set the lists equal,
        else append the home to the list
        :param new_home: New home to add to the list
        """
        if isinstance(new_home, list):
            self._homes = new_home
        else:
            self._homes.append(new_home)

    @property
    def destinations(self):
        """
        Get the list of destinations stored
        :return:
        """
        return self._destinations

    @destinations.setter
    def destinations(self, new_destination):
        self._destinations.append(new_destination)
