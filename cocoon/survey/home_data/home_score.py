from cocoon.commutes.models import ZipCodeBase, ZipCodeChild

from cocoon.commutes.constants import GoogleCommuteNaming
from cocoon.survey.constants import AVERAGE_BICYCLING_SPEED, AVERAGE_WALKING_SPEED, EXTRA_DISTANCE_LAT_LNG_APPROX
import geopy.distance

import math


class HomeScore(object):
    # noinspection SpellCheckingInspection
    """
        Class stores a home with supporting information regarding the home. Keeps track of data
            while the algorithm is being computed

          Attributes:
            self._home (RentDatabasemodel): The actual home specified from the house database models.
            self._accumulated_points (int): The total amount of points this home has earned
            self._total_possible_points (int): The total amount of points this home could have earned
            self._approx_commute_times_minutes (dict{'(Destinationmodel)', (int)}: A dictionary with the key being
                the destination and the value is the approximate commute time to that destination in minutes
            self._exact_commute_times_minutes (dict{'(DestinationModel)', (int)}: A dictionary with the key being
                the destination and the value is the exact commute time to that destination in minutes
            self._eliminated (boolean): Indicates whether or not the home has been eliminated already

        """

    def __init__(self, new_home=None):
        self._home = new_home
        self._accumulated_points = 0
        self._total_possible_points = 0
        self._approx_commute_times_minutes = {}
        self._exact_commute_times_minutes = {}
        self._eliminated = False

    @property
    def eliminated(self):
        """
        Returns whether or not the home has been eliminated
        :return: (Boolean): True if the home is eliminated or false if it hasn't
        """
        return self._eliminated

    @eliminated.setter
    def eliminated(self, is_eliminated):
        """
        Sets whether or not the home has been eliminated
        :param is_eliminated: (Boolean): True if the home is eliminated or false if it isn't
        """
        self._eliminated = is_eliminated

    def eliminate_home(self):
        """
        Eliminates the homes
        """
        self.eliminated = True

    @property
    def home(self):
        """
        Returns the home that is stored in the HomeScore
        :return: (RentDatabaseModel): The home stored in the home score class
        """
        return self._home

    @home.setter
    def home(self, new_home):
        """
        Sets a home in the home score class
        :param new_home: (RentDatabaseModel): The new home to store in the home score class
        """
        self._home = new_home

    @property
    def approx_commute_times(self):
        """
        Returns the approx_commute_times
        :return: (dict{DestinationModel, int}): The approximate commute times
        """
        return self._approx_commute_times_minutes

    @approx_commute_times.setter
    def approx_commute_times(self, new_approx_commute_time):
        """
        Takes in a dictionary of commutes and adds the ones that do not exist
            to the member dictionary
        :param new_approx_commute_time (dict{DestinationModel, int}): Dictionary of Destinations and commute times in
            in minutes to be added to the home
        """
        self._approx_commute_times_minutes.update(new_approx_commute_time)

    @property
    def exact_commute_times(self):
        """
        Returns the exact commute times
        :return: (dict{DestinationModel, (int)}): Returns a dictionary of the Destination and the corresponding time
        """
        return self._exact_commute_times_minutes

    @exact_commute_times.setter
    def exact_commute_times(self, new_exact_commute_time):
        """
        Takes in a dictionary of commutes and adds the ones that do not exist
            to the member dictionary
        :param new_approx_commute_time (dict{DestinationModel, (int)}): Dictionary of Destinations and commute times in
            in minutes to be added to the home
        """
        self._exact_commute_times_minutes.update(new_exact_commute_time)

    def populate_approx_commutes(self, home, destination, lat_lng_dest=""):
        """
        Based on the commute type of the destination, this function determines the algorithm method that will
            be used to generate the approximation
        :param home: (RentDatabaseModel) -> The home that the user is computing for
        :param destination: (DestinationModel): The destination as a RentingDestinationsModel object
        :param lat_lng_dest: ((decimal, decimal)): -> A Tuple of (latitude, longitude) for the destination
        :return (Boolean): True if a valid pair match is found, False otherwise.
        """
        if destination.commute_type.commute_type == GoogleCommuteNaming.DRIVING:
            return self.zip_code_approximation(home.zip_code, destination)
        elif destination.commute_type.commute_type == GoogleCommuteNaming.TRANSIT:
            return self.zip_code_approximation(home.zip_code, destination)
        elif destination.commute_type.commute_type == GoogleCommuteNaming.BICYCLING:
            return self.lat_lng_approximation(home, destination, lat_lng_dest, AVERAGE_BICYCLING_SPEED)
        elif destination.commute_type.commute_type == GoogleCommuteNaming.WALKING:
            return self.lat_lng_approximation(home, destination, lat_lng_dest, AVERAGE_WALKING_SPEED)

    def lat_lng_approximation(self, home, destination, lat_lng_dest, average_speed):
        """
        This function given a home and a destination will determine the distance between the two homes based off of the
            lat and lng points. Then once the distance is determined, then the commute time is determined based off of
            the average speed.
        :param home: (RentDatabaseModel) -> The home that the user is computing for
        :param destination: (DestinationModel): The destination as a RentingDestinationsModel object
        :param lat_lng_dest: ((decimal, decimal)): -> A Tuple of (latitude, longitude) for the destination
        :param average_speed: (int) -> The average speed in mph that the person moves for the given mode of transport
        :return: (Boolean): -> True: The home approximation was found and added
                               False: The home was not able to have a approximation created
        """
        # Stores the lat and lng points for the home
        lat_lng_home = (home.latitude, home.longitude)

        # Returns the distance from the two lat lng points in miles
        distance = geopy.distance.geodesic(lat_lng_home, lat_lng_dest).miles

        # If the distance is less than a mile then don't add any distance since it is already so close
        if distance > 1:
            # Extra distance is determined by giving more distance to homes farther away
            extra_distance = EXTRA_DISTANCE_LAT_LNG_APPROX * (1 - 1.0/distance)
            # This normalizes the value since walking needs less of a weight than biking since homes
            #   are more direct when walking.
            distance += extra_distance * average_speed/AVERAGE_BICYCLING_SPEED
        if average_speed is not 0:
            commute_time_hours = distance / average_speed
            commute_time = commute_time_hours * 60
        else:
            return False
        self.approx_commute_times[destination] = commute_time
        return True

    def zip_code_approximation(self, origin_zip, destination):
        """
        This is the zip_code_approximation algorithm. This assumes that the zip-code cache is already updated
            and that all the valid pairs are already generated. This just goes through and finds the valid pairs
            for the given zip_code and the destination
        :param origin_zip: (string) -> The zip code of the origin, i.e home
        :param destination: (DestinationModel): The destination as a RentingDestinationsModel object
        :return (Boolean): True if a valid pair exists, False otherwise.
        """
        parent_zip_code_dictionary = ZipCodeBase.objects.filter(zip_code__exact=origin_zip)
        if parent_zip_code_dictionary.exists():
            for parent in parent_zip_code_dictionary:
                zip_code_dictionary = ZipCodeChild.objects.filter(
                    base_zip_code_id=parent).filter(zip_code__exact=destination.zip_code) \
                    .filter(commute_type=destination.commute_type)
                if zip_code_dictionary.exists():
                    for match in zip_code_dictionary:
                        if match.zip_code_cache_still_valid():
                            self.approx_commute_times[destination] = match.commute_time_minutes
                            return True
                        else:
                            return False
                else:
                    return False
        else:
            return False

    @property
    def accumulated_points(self):
        """
        Returns the accumulated_points
        :return: (int): The amount of points the home has earned
        """
        return self._accumulated_points

    @accumulated_points.setter
    def accumulated_points(self, new_points):
        """
        Adds more points to the accumulated_points
        :param new_points: (int): The amount of points to add
        """
        self._accumulated_points += new_points

    @property
    def total_possible_points(self):
        """
        Returns the total_possible_points
        :return: (int): The amount of points the home could have earned
        """
        return self._total_possible_points

    @total_possible_points.setter
    def total_possible_points(self, new_possible_points):
        """
        Adds more points to the total_possible_points
        :param new_possible_points: (int): The amount of points to add
        """
        self._total_possible_points += new_possible_points

    def percent_score(self):
        """
        Generates the score percentage
        :return: (int): The percent fit the home is, 100 being perfect, 0 being the worst
        """
        if self.eliminated:
            return -1
        elif self.accumulated_points < 0 or self.total_possible_points < 0:
            return -1
        elif self.total_possible_points != 0:
            return (self.accumulated_points / self.total_possible_points) * 100
        else:
            return 0

    def user_friendly_score(self):
        """
        Produces a user friendly version of the percent score
        :return: (int) The score percent rounded to the nearest int
        """
        return round(self.percent_score())
