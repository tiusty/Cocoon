class HomeCommute(object):

    def __init__(self, zip_code, state):
        self.zip_code = zip_code
        self.state = state

    @staticmethod
    def home_score_to_home_cache(homes):
        """
        Converts a list of home scores to the home cache class
        :param homes: (list(HomeScore)) -> The homes to convert
        :return: (list(HomeCommute)) -> The homes in the appropriate format for the approximation
        """
        home_cache = []
        for home in homes:
            home_cache.append(HomeCommute(home.home.zip_code, home.home.state))
        return home_cache

    @staticmethod
    def destination_to_home_cache(destination):
        """
        Converts a destination model into a home cache object
        :param destination: (destinationModel) -> The destination to convert
        :return: (HomeCommute) -> The destination in the home cache format
        """
        return HomeCommute(destination.zip_code, destination.state)

    @staticmethod
    def rentdatabases_to_home_cache(homes):
        """
        Convert a list of rentdatabases to home cache object
        :param homes: (list(RentDatabase model)) -> The homes to convert
        :return: (list(HomeCommute)) -> The homes in the correct format
        """
        home_cache = []
        for home in homes:
            home_cache.append(HomeCommute(home.zip_code, home.state))
        return home_cache

    @staticmethod
    def rentdatabase_to_home_cache(home):
        """
        Convert a rentdatabase to home cache object
        :param home: (RentDatabase model) -> The homes to convert
        :return: (HomeCommute) -> The homes in the correct format
        """
        return HomeCommute(home.zip_code, home.state)

