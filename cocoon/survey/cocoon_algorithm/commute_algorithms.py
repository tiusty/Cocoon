# Import survey constants
from cocoon.survey.constants import APPROX_COMMUTE_RANGE, COMMUTE_QUESTION_WEIGHT


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
        self._approx_commute_range_minutes = APPROX_COMMUTE_RANGE
        self.destinations = []
        self.commute_question_weight = COMMUTE_QUESTION_WEIGHT
        # TODO: Set the min_possible_commute from global config file. Also add implementation for min_possible_commute
        self._min_possible_commute = 11
        # Need super to allow calling each classes constructor
        super(CommuteAlgorithm, self).__init__()

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

    def populate_commute_algorithm(self, user_survey):
        # Retrieves all the destinations that the user recorded
        self.destinations = user_survey.tenants.all()

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
            if (approx_commute_times[commute] > commute.max_commute + self.approx_commute_range) \
                            or (approx_commute_times[commute] < commute.min_commute - self.approx_commute_range):
                return False
        return True

    @staticmethod
    def compute_commute_score(commute_minutes, commuter):
        """
        Compute the score based off the commute. A percent value of the fit of the home is returned.
        I.E, .67, .47, etc will be returned. The scaling will be done in the parent class
        Note: Since the eliminating filter should have been done first, this computation
            does not mark any home for elimination
        :param commute_minutes: (int): The commute time in minutes.
        :param commuter: (RentingDestinationModel): The renting destination model which holds all the information
            regarding the commute
        :return: (float) THe percent fit the home is or -1 if the home should be eliminated
        """

        # Because the commute is allowed to be less or more depending on the approx_commute_range
        #   the homes are allowed to be past the user bounds. Therefore if the commute is past the bounds,
        #   just set the home to the max or min
        if commute_minutes < commuter.min_commute:
            commute_minutes = commuter.min_commute
        elif commute_minutes > commuter.max_commute:
            commute_minutes = commuter.max_commute

        commute_time_normalized = commute_minutes - commuter.desired_commute
        commute_range = commuter.max_commute - commuter.desired_commute

        # Anything below the desired_commute gets a 100
        if commute_minutes <= commuter.desired_commute:
            return 1
        # if the commute range is 0 then it only gets 100 if the
        #   commute time is equal to the desired time then it gets 100 otherwise a 0
        elif commute_range <= 0:
            if commute_minutes == commuter.desired_commute:
                return 1
            else:
                return 0

        return 1 - (commute_time_normalized / commute_range)
