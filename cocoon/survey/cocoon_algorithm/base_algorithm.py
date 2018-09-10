# Import Python Modules
from django.utils import timezone

# Import Django modules
from django.db.models import Q

# Import houseDatabase modules
from cocoon.houseDatabase.models import RentDatabaseModel, HomeTypeModel, MlsManagementModel, HomeProviderModel

# Import HomeScore class
from cocoon.survey.home_data.home_score import HomeScore


class CocoonAlgorithm(object):
    """
    Class included the base values for any algorithm.

      Attributes:
        self._homes (List[HomeScore]): Stores a list of homes as a HomeScore. These are the possible homes the user
            could live in
    """

    def __init__(self):
        self._homes = []
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

    def populate_survey_homes(self, user_survey):
        """
        Populates the homes variable based off a user survey
        :param user_survey: (RentingSurveyModel): The survey filled out by the user
        """

        # Find all the possible homes that fit the static filter
        filtered_home_list = self.generate_static_filter_home_list(user_survey)

        # Add homes to rent_algorithm, homes should be stored as a HomeScore
        for home in filtered_home_list:
            self.homes = HomeScore(home)

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

        current_home_providers = []
        for house in user_survey.provider.all():
            current_home_providers.append(house.provider)

        provider_queries = [Q(listing_provider_home=value) for value in
                            HomeProviderModel.objects.filter(provider__in=current_home_providers)]

        # Logic Or all the provider queries together, to make one query
        if current_home_providers:
            query_provider = provider_queries.pop()
            for item in provider_queries:
                query_provider |= item

        # Query the database
        house_query =  RentDatabaseModel.objects\
            .filter(price_home__range=(user_survey.min_price, user_survey.max_price)) \
            .filter(query_home_type) \
            .filter(currently_available_home=True) \
            .filter(num_bedrooms_home=user_survey.num_bedrooms) \
            .filter(num_bathrooms_home__range=(user_survey.min_bathrooms, user_survey.max_bathrooms))

        if current_home_providers:
            house_query = house_query.filter(query_provider)

        return house_query
