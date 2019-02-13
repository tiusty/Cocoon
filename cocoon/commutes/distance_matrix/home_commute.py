class HomeCommute(object):

    def __init__(self, zip_code='', state='', address='', city='', valid=True):
        self.zip_code = zip_code
        self.state = state
        self.address = address
        self.city = city
        self.valid = valid

    def return_commute(self):
        if self.address and self.city and self.state:
            return self.return_full_address()
        else:
            return self.return_zip_code()

    def return_zip_code(self):
        if self.valid:
            return self.zip_code
        else:
            return ''

    def return_full_address(self):
        if self.valid and self.address and self.city and self.state and self.zip_code:
            return "{0}, {1}, {2}, {3}".format(self.address, self.city, self.state, self.zip_code)
        elif self.valid and self.address and self.city and self.state:
            return "{0}, {1}, {2}".format(self.address, self.city, self.state)
        else:
            return ''


    @staticmethod
    def home_scores_to_home_commute(homes):
        """
        Converts a list of home scores to the home cache class
        :param homes: (list(HomeScore)) -> The homes to convert
        :return: (list(HomeCommute)) -> The homes in the appropriate format for the approximation
        """
        home_cache = []
        for home in homes:
            home_cache.append(HomeCommute(zip_code=home.home.zip_code, state=home.home.state, address=home.home.street_address, city=home.home.city))
        return home_cache

    @staticmethod
    def destination_to_home_commute(destination):
        """
        Converts a destination model into a home cache object
        :param destination: (destinationModel) -> The destination to convert
        :return: (HomeCommute) -> The destination in the home cache format
        """
        return HomeCommute(zip_code=destination.zip_code, state=destination.state, address=destination.street_address, city=destination.city)

    @staticmethod
    def rentdatabases_to_home_commute(homes):
        """
        Convert a list of rentdatabases to home cache object
        :param homes: (list(RentDatabase model)) -> The homes to convert
        :return: (list(HomeCommute)) -> The homes in the correct format
        """
        home_cache = []
        for home in homes:
            home_cache.append(HomeCommute(zip_code=home.zip_code, state=home.state, address=home.street_address, city=home.city))
        return home_cache

    @staticmethod
    def rentdatabase_to_home_commute(home):
        """
        Converts a rentdatabase to home cache object
        :param home: (RentDatabase model) -> The homes to convert
        :return: (HomeCommute) -> The homes in the correct format
        """
        return HomeCommute(zip_code=home.zip_code, state=home.state, address=home.street_address, city=home.city)

    @staticmethod
    def zipcodes_to_home_commute(zipcode_list):
        zipcodes = []
        for zipcode in zipcode_list:
            zipcodes.append(HomeCommute(zipcode))
        return zipcodes
