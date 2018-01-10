from houseDatabase.models import ZipCodeDictionaryParentModel, ZipCodeDictionaryChildModel

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

    def __init__(self, new_home):
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

    def populate_approx_commutes(self, origin_zip, destination, commute_type):
        """
        Queries the ZipCode database to attempt to populate this HomeScore's approximate commute dictionary.
        Returns True on success, False on failure.
        :param destination: (DestinationModel): The destination as a RentingDestinationsModel object
        :param commute_type: (String) commute_type enum, eg. "Driving"
        :return (Boolean): True on success, False on failure.
        """
        parent_zip_code_dictionary = ZipCodeDictionaryParentModel.objects.filter(zip_code_parent__exact=origin_zip)
        if parent_zip_code_dictionary.exists():
            for parent in parent_zip_code_dictionary:
                zip_code_dictionary = ZipCodeDictionaryChildModel.objects.filter(
                    parent_zip_code_child_id=parent).filter(zip_code_child__exact=destination.zip_code)\
                    .filter(commute_type_child__exact=commute_type)
                if zip_code_dictionary.exists():
                    for match in zip_code_dictionary:
                        if match.zip_code_cache_still_valid():
                            self.approx_commute_times[destination.destination_key] = match.commute_time_minutes
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
