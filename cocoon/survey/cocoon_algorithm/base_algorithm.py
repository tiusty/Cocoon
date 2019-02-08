# Import Python Modules
from datetime import timedelta
from django.db.models import F

# Import houseDatabase modules
from cocoon.houseDatabase.models import RentDatabaseModel
from cocoon.survey.constants import MOVE_WEIGHT_MAX

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
            # Only add homes that fall within the users polygon
            if self.polygon_filter(home, polygons, user_survey.polygon_filter_type):
                self.homes = HomeScore(home)

    @staticmethod
    def generate_polygons(survey):
        """
        Generates all the polygons the user created. Converts the polygons from the django database version
            to shapely polygons
        :param survey: (RentingSurvey) -> The survey
        :return: (list(shapely.polygons)) -> The list of polygons that are formatted to shapely
        """
        polygons = []
        for polygon_model in survey.polygons.all():
            vertices = []
            for vertices_model in polygon_model.vertices.all():
                vertices.append((vertices_model.lat, vertices_model.lng))
            polygon = Polygon(vertices)
            polygons.append(polygon)
        return polygons

    @staticmethod
    def polygon_filter(home, polygons, filter_type):
        """
        Determines if a home is within any of the polygons the user created
        :param home: (RentDatabaseModel) -> The home that is being tested
        :param polygons: (list(shapely.polygons)) -> The list of polygons the user created
        :param filter_type: (int) -> The filter type the user desires
        :return: (boolean) -> Whether the home is within the polygon or not
        """

        # If the user selected draw on map then filter based on the polygons the user drew
        if filter_type is 1 and len(polygons) > 0:
            point = Point(home.latitude, home.longitude)
            result = False
            for polygon in polygons:
                if polygon.contains(point):
                    result = True
                    break
        else:
            result = True

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
            .filter(num_bedrooms=user_survey.num_bedrooms) \
            .filter(home_type__in=user_survey.home_type.all())\

        # Depending on the user move weight, determine how the static filter works
        if user_survey.move_weight == MOVE_WEIGHT_MAX:
            house_query = house_query.filter(currently_available=True)
        else:
            house_query = house_query.filter(
                date_available__range=(
                    user_survey.earliest_move_in - timedelta(days=7),
                    user_survey.latest_move_in + timedelta(days=2)))

        return house_query
