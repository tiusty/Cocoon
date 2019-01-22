# Import survey constants
from cocoon.survey.constants import APPROX_COMMUTE_RANGE, COMMUTE_QUESTION_WEIGHT, MIN_COMMUTE_TIME


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
        self._commute_type (str): The type of commute specified by the user

     """

    def __init__(self):
        """
        Sets the values to default values. Calls the super function so all parent init functions are called.
        """
        # Need super to allow calling each classes constructor
        super(CommuteAlgorithm, self).__init__()
        self.tenants = []
        self.approx_commute_range = APPROX_COMMUTE_RANGE  # Minutes
        self.commute_question_weight = COMMUTE_QUESTION_WEIGHT

    def populate_commute_algorithm(self, user_survey):
        """
        Adds all the tenants from the survey to the class
        :param user_survey: (RentSurveyModel) -> The survey the user took
        """
        # Retrieves all the tenants that the user recorded
        self.tenants = user_survey.tenants.all()

    def approximate_commute_filter(self, approx_commute_times):
        """
        Returns whether or not the approximate commute times are within the
        user acceptable range. If any of the commutes are not within the acceptable
        range, then False is returned. Thought if it is below the min_commute then it is eliminated
        :param approx_commute_times: (dict{(Destination):(int)}): A dictionary containing the destinationModel as the
            and the value as the commute time in minutes to that destination
        :return: (Boolean): True if the home is inside the range, False otherwise
        """
        for commute in approx_commute_times:
            if (approx_commute_times[commute] > commute.max_commute + self.approx_commute_range) \
                            or approx_commute_times[commute] < commute.min_commute:
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
