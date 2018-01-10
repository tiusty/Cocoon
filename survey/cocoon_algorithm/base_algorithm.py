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
        self._homes (List[HomeScore]): Stores a list of homes as a HomeScore. These are the possible homes the user
            could live in
        self._destinations (DestinationsModel Queryset): The desired destinations
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
        :return: ([HomeScore]) -> List of HomeScore
        """
        return self._homes

    @homes.setter
    def homes(self, new_home):
        """
        Add home to homes list.
        If the variable is a list, then set the lists equal,
        else append the home to the list
        :param new_home: ([HomeScore] or HomeScore): new HomeScore to add either individual or as a list
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
        :return: (DestinationModel Queryset): The list of destinations the user specified
        """
        return self._destinations

    @destinations.setter
    def destinations(self, new_destination):
        """
        Add destinations to the class
        :param new_destination: (DestinationModel Queryset): Sets the variable with a new query set
        """
        self._destinations = new_destination

    def populate_survey_destinations_and_possible_homes(self, user_survey):
        """
        Populates the homes variable and destinations variable based off a user survey
        :param user_survey: (RentingSurveyModel): The survey filled out by the user
        """

        # Find all the possible homes that fit the static filter
        filtered_home_list = self.generate_static_filter_home_list(user_survey)

        # Add homes to rent_algorithm, homes should be stored as a HomeScore
        for home in filtered_home_list:
            self.homes = HomeScore(home)

        # Retrieves all the destinations that the user recorded
        self.destinations = user_survey.rentingdestinationsmodel_set.all()

    @staticmethod
    def generate_static_filter_home_list(user_survey):
        """
        Finds all the homes that fit the user survey based on static filtering.
        :param user_survey: (RentingSurveyModel): The survey filled out by the user
        :return: (RentDataBaseModel Queryset): All the homes that fit the static filter
        """

        # Find all the home types the user desires
        current_home_types = []
        for home in user_survey.home_type.all():
            current_home_types.append(home.home_type)

        # Create queries for all the user home types desired
        home_type_queries = [Q(home_type_home=value) for value in
                             HomeTypeModel.objects.filter(home_type_survey__in=current_home_types)]

        # Logic Or all the home type queries together, to make one query
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
