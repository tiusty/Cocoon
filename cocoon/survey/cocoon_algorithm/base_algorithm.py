# Import Python Modules
from django.utils import timezone
from django.db.models import F

# Import houseDatabase modules
from cocoon.houseDatabase.models import RentDatabaseModel

# Import HomeScore class
from cocoon.survey.home_data.home_score import HomeScore

# Import Python Modules
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


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
        polygons = self.generate_polygons(user_survey)
        for home in filtered_home_list:
            if self.polygon_filter(home, polygons):
                self.homes = HomeScore(home)

    @staticmethod
    def generate_polygons(survey):
        polygons = []
        for polygon_model in survey.polygons.all():
            vertices = []
            for vertices_model in polygon_model.vertices.all():
                vertices.append((vertices_model.lat, vertices_model.lng))
            polygon = Polygon(vertices)
            polygons.append(polygon)
        return polygons

    @staticmethod
    def polygon_filter(home, polygons):
        point = Point(home.latitude, home.longitude)
        result = False
        for polygon in polygons:
            if polygon.contains(point):
                result = True
                break

        return result

    @staticmethod
    def generate_static_filter_home_list(user_survey):
        """
        Finds all the homes that fit the user survey based on static filtering.
        :param user_survey: (RentingSurveyModel): The survey filled out by the user
        :return: (RentDataBaseModel Queryset): All the homes that fit the static filter
        """
        # Query the database
        house_query = RentDatabaseModel.objects\
            .filter(last_updated=F('listing_provider__last_updated_feed')) \
            .filter(price__range=(user_survey.min_price, user_survey.max_price)) \
            .filter(currently_available=True) \
            .filter(num_bedrooms=user_survey.num_bedrooms) \
            .filter(num_bathrooms__range=(user_survey.min_bathrooms, user_survey.max_bathrooms)) \
            .filter(home_type__in=user_survey.home_type.all())

        return house_query
