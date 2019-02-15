from cocoon.houseDatabase.serializers import RentDatabaseSerializer


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
        self.missing_amenities = []

    @property
    def percent_match(self):
        """
        Generates the percent match
        :return: (int): The percent fit the home is, 100 being perfect, 0 being the worst
        """
        if self.accumulated_points < 0 or self.total_possible_points < 0:
            return -1
        elif self.total_possible_points != 0:
            return (self.accumulated_points / self.total_possible_points) * 100
        else:
            return 0

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

    def eliminate_home(self, missing_amenity=None):
        """
        Eliminates the homes
        """
        if missing_amenity is not None:
            if missing_amenity not in self.missing_amenities:
                self.missing_amenities.append(missing_amenity)
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
        # if self.eliminated:
        #     return -1
        if self.accumulated_points < 0 or self.total_possible_points < 0:
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

    def letter_grade(self):
        if self.percent_score() > 97:
            return "A+"
        elif self.percent_score() > 93:
            return "A"
        elif self.percent_score() > 90:
            return "A-"
        elif self.percent_score() > 87:
            return "B+"
        elif self.percent_score() > 83:
            return "B"
        elif self.percent_score() > 80:
            return "B-"
        elif self.percent_score() > 77:
            return "C+"
        elif self.percent_score() > 73:
            return "C"
        elif self.percent_score() > 70:
            return "C-"
        elif self.percent_score() > 66:
            return "D+"
        elif self.percent_score() > 63:
            return "D"
        elif self.percent_score() > 60:
            return "D-"
        elif self.percent_score() > 57:
            return "F+"
        elif self.percent_score() > 54:
            return "F"
        elif self.percent_score() > 0:
            return "F-"
        else:
            return "N/R"

