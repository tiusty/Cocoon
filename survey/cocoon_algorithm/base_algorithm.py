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
        :return: [HomeScore] -> List of HomeScore
        """
        return self._homes

    @homes.setter
    def homes(self, new_home):
        """
        Add home to homes list.
        If the variable is a list, then set the lists equal,
        else append the home to the list
        :param new_home: [HomeScore] or HomeScore -> new HomeScore to add either individual or as a list
        """
        # If a list is provided then set the lists equal
        if isinstance(new_home, list):
            self._homes = new_home
        # If a single element is provided then append that element
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
        """
        Add destinations to the class
        :param new_destination: survey.RentingDestinationModel as a list or single element
        """
        # If a list is provided then set the lists equal
        if isinstance(new_destination, list):
            self._destinations = new_destination
        # If a single element is provided then append that element
        else:
            self._destinations.append(new_destination)
