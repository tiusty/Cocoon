from Cocoon.settings.Global_Config import commute_question_weight
from commutes.models import CommuteType


class CommuteAlgorithm(object):
    """
    Class includes important commute variables and supporting functions.
    Meant to be used in conjunction with a base algorithm class.

     Attributes:
        self._approx_commute_range_minutes (int): The amount of minutes from the commute time which is acceptable for
            the approximation.
        self._max_user_commute_minutes (int): The max # of minutes allowed for a commute (not including range)
        self._min_user_commute_minutes (int): The min # of minutes allowed for a commute (not including range)
        self._commute_user_scale_factor (int): The user defined scale for the commute factor
        self._commute_question_weight (int): The cocoon defined scale for the commute factor, should be loaded from
            global config file
        self._min_possible_commute (int): The amount of minutes which everything below will be 100% match
        self._commute_type (str): The type of commute specified by the user

     """

    def __init__(self):
        """
        Sets the values to default values. Calls the super function so all parent init functions are called.
        """
        self._approx_commute_range_minutes = 0
        self._max_user_commute_minutes = 0
        self._min_user_commute_minutes = 0
        self._commute_user_scale_factor = 1
        self._commute_question_weight = commute_question_weight
        # TODO: Set the min_possible_commute from global config file. Also add implementation for min_possible_commute
        self._min_possible_commute = 11
        # Note: This means the driving object needs to be created before this class is run
        self._commute_type_query = CommuteType.objects.get(commute_type_field='Driving')
        # Need super to allow calling each classes constructor
        super(CommuteAlgorithm, self).__init__()

    def populate_commute_algorithm_information(self, user_commute_scale, user_max_commute_minutes,
                                               user_min_commute_minutes, user_commute_type):
        """
        Function sets important constants for commute algorithm
        :param user_commute_scale: (int): The user commute scale factor
        :param user_max_commute_minutes: (int): The max time the user is willing to spend commuting in minutes
        :param user_min_commute_minutes: (int): The min time the user is willing to spend commuting in minutes
        :param user_commute_type: (CommuteTypeModel): The commute type desired by the user
        :return:
        """
        self.max_user_commute = user_max_commute_minutes
        self.min_user_commute = user_min_commute_minutes
        self.commute_user_scale_factor = user_commute_scale
        self.commute_type_query = user_commute_type

    @property
    def commute_type_query(self):
        """
        Returns the commute type
        :return: (CommuteTypeModel): Returns the commute type
        """
        return self._commute_type_query

    @commute_type_query.setter
    def commute_type_query(self, new_commute_type):
        """
        Sets the commute type
        :param new_commute_type: (CommuteTypeModel): The new commute type desired by the user
        """
        self._commute_type_query = new_commute_type

    @property
    def commute_question_weight(self):
        """
        Gets the commute_question_weight
        :return: (int)L The commute_question_weight
        """
        return self._commute_question_weight

    @commute_question_weight.setter
    def commute_question_weight(self, new_commute_question_weight):
        """
        Sets the commute_question_weight
        :param new_commute_question_weight: (int): The new commute question weight
        """
        self._commute_question_weight = new_commute_question_weight

    @property
    def min_possible_commute(self):
        """
        Returns the min_possible_commute
        :return: (int): Returns the min possible commute
        """
        return self._min_possible_commute

    @min_possible_commute.setter
    def min_possible_commute(self, new_min_possible_commute):
        """
        Sets the min_possible_commute.
        :param new_min_possible_commute: (int): The new min possible commute
        """
        self._min_possible_commute = new_min_possible_commute

    @property
    def commute_user_scale_factor(self):
        """
        Gets the commute user scale factor.
        This increases or decreases the weight that the commute has to the survey
        :return: (int): Te commute user scale factor
        """
        return self._commute_user_scale_factor

    @commute_user_scale_factor.setter
    def commute_user_scale_factor(self, new_commute_user_scale_factor):
        """
        Sets the commute user scale factor
        :param new_commute_user_scale_factor: (int): The new scale factor as an int
        """
        self._commute_user_scale_factor = new_commute_user_scale_factor

    @property
    def approx_commute_range(self):
        """
        Approx commute range is the +/- of the acceptable commute range
        Therefore it the user desires 40-80 min commute, if the approx_commute range is 20,
        then the range becomes 20-100 minutes. This is due to the approximations of zip codes.
        Approx_commute_range is stored as minutes
        :return: (int): the approx_commute_range in minutes
        """
        return self._approx_commute_range_minutes

    @approx_commute_range.setter
    def approx_commute_range(self, new_approx_commute_range_minutes):
        """
        Set the approx_commute range in minutes
        :param new_approx_commute_range_minutes: (int): The new approx commute range in minutes
        """
        if new_approx_commute_range_minutes < 0:
            self._approx_commute_range_minutes = 0
        else:
            self._approx_commute_range_minutes = new_approx_commute_range_minutes

    @property
    def max_user_commute(self):
        """
        Get the max_user_commute as minutes.
        This is the maximum commute that a user is willing to have
        :return: (int): The max commute time in minutes
        """
        return self._max_user_commute_minutes

    @max_user_commute.setter
    def max_user_commute(self, new_max_user_commute_minutes):
        """
        Sets the max_user_commute as minutes
        :param new_max_user_commute_minutes: (int) The new max_commute_time in minutes
        """
        self._max_user_commute_minutes = new_max_user_commute_minutes

    @property
    def min_user_commute(self):
        """
        Get the min_user_commute as minutes
        This is the minimum commute that user is willing to have
        :return: (int): The min commute time in minutes
        """
        return self._min_user_commute_minutes

    @min_user_commute.setter
    def min_user_commute(self, new_min_user_commute):
        """
        Set the min_user_commute as minutes
        :param new_min_user_commute: (int): The new min commute time as minutes
        """
        self._min_user_commute_minutes = new_min_user_commute

    def compute_approximate_commute_filter(self, approx_commute_times):
        """
        Returns whether or not the approximate commute times are within the
        user acceptable range. If any of the commutes are not within the acceptable
        range, then False is returned
        :param approx_commute_times: (dict{(Destination):(int)}): A dictionary containing the destinationModel as the
            and the value as the commute time in minutes to that destination
        :return: (Boolean): True if the home is inside the range, False otherwise
        """
        for commute in approx_commute_times:
            if (approx_commute_times[commute] > self.max_user_commute + self.approx_commute_range) \
                            or (approx_commute_times[commute] < self.min_user_commute - self.approx_commute_range):
                return False
        return True

    def compute_commute_score(self, commute_minutes):
        """
        Compute the score based off the commute. A percent value of the fit of the home is returned.
        I.E, .67, .47, etc will be returned. The scaling will be done in the parent class
        Note: Since the eliminating filter should have been done first, this computation
            does not mark any home for elimination
        :param commute_minutes: (int): The commute time in minutes.
        :return: (float) THe percent fit the home is or -1 if the home should be eliminated
        """

        # Because the commute is allowed to be less or more depending on the approx_commute_range
        #   the homes are allowed to be past the user bounds. Therefore if the commute is past the bounds,
        #   just set the home to the max or min
        if commute_minutes < self.min_user_commute:
            commute_minutes = self.min_user_commute
        elif commute_minutes > self.max_user_commute:
            commute_minutes = self.max_user_commute

        commute_time_normalized = commute_minutes - self.min_user_commute
        commute_range = self.max_user_commute - self.min_user_commute

        if commute_range <= 0:
            if commute_minutes == self.min_user_commute:
                return 1
            else:
                return 0

        return 1 - (commute_time_normalized / commute_range)
