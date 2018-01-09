# Import Django modules
from django.db.models import Q

# Import houseDatabase modules
from houseDatabase.models import RentDatabaseModel, HomeTypeModel

# Import HomeScore class
from survey.home_data.home_score import HomeScore


class CocoonAlgorithm(object):
    """
    Class included the base values for any algorithm.

      Attributes:
        self._homes (List[HomeScore]): Stores a list of homes as a HomeScore
        self._destinations (List[anything that inherits survey.models.DestinationsModel]): The desired destinations
            specified by the user. These locations are the work, schools that the user needs to go to.

    """

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
        :param new_destination: survey.RentingDestinationModel as a Query Set
        """
        self._destinations = new_destination

    def populate_survey_destinations_and_possible_homes(self, user_survey):

        # Find all the possible homes that fit the static filter
        filtered_home_list = self.generate_static_filter_home_list(user_survey)

        # Add homes to rent_algorithm
        for home in filtered_home_list:
            self.homes = HomeScore(home)

        # Retrieves all the destinations that the user recorded
        self.destinations = user_survey.rentingdestinationsmodel_set.all()

    @staticmethod
    def generate_static_filter_home_list(user_survey):
        """
        Compute Static Elements
        The item that will filter the list the most should be first to narrow down the number of iterations
        The database needs to be searched
        (Right now it isn't order by efficiency but instead by when it was added. Later it can be switched around

        Current order:
        1. Filter by price range. The House must be in the correct range to be accepted
        2. Filter by Home Type. The home must be the correct home type to be accepted
        3. Filter by Move In day. The two move in days create the range that is allowed. The range is inclusive
            If the house is outside the range it is eliminated
        4. Filter by the number of bed rooms. It must be the correct number of bed rooms to work.
        4. Filter by the number of bathrooms
        """

        # Find all the home types the user desires
        current_home_types = []
        for home in user_survey.home_type.all():
            current_home_types.append(home.home_type)

        # Create queries for all the user home types desired
        home_type_queries = [Q(home_type_home=value) for value in
                             HomeTypeModel.objects.filter(home_type_survey__in=current_home_types)]

        # Or all the home type queries together, to make one query
        query_home_type = home_type_queries.pop()
        for item in home_type_queries:
            query_home_type |= item

        # Query the database
        return RentDatabaseModel.objects \
            .filter(price_home__range=(user_survey.min_price, user_survey.max_price)) \
            .filter(query_home_type) \
            .filter(move_in_day_home__range=(user_survey.move_in_date_start, user_survey.move_in_date_end)) \
            .filter(num_bedrooms_home=user_survey.num_bedrooms) \
            .filter(num_bathrooms_home__range=(user_survey.min_bathrooms, user_survey.max_bathrooms))

