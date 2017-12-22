from Unicorn.settings.Global_Config import commute_question_weight


class CommuteAlgorithm(object):

    def __init__(self):
        self._approx_commute_range_minutes = 0
        self._max_user_commute_minutes = 0
        self._min_user_commute_minutes = 0
        self._commute_user_scale_factor = 1
        self._commute_question_weight = commute_question_weight
        # TODO: Set the min_possible_commute from global config file. Also add implementation for min_possible_commute
        self._min_possible_commute = 11
        # Need super to allow calling each classes constructor
        super(CommuteAlgorithm, self).__init__()

    @property
    def commute_question_weight(self):
        return self._commute_question_weight

    @commute_question_weight.setter
    def commute_question_weight(self, new_commute_question_weight):
        self._commute_question_weight = new_commute_question_weight

    @property
    def min_possible_commute(self):
        return self._min_possible_commute

    @min_possible_commute.setter
    def min_possible_commute(self, new_min_possible_commute):
        self._min_possible_commute = new_min_possible_commute

    @property
    def commute_user_scale_factor(self):
        """
        Gets the commute user scale factor.
        This increases or decreases the weight that the commute has to the survey
        :return: THe commute user scale factor
        """
        return self._commute_user_scale_factor

    @commute_user_scale_factor.setter
    def commute_user_scale_factor(self, new_commute_user_scale_factor):
        """
        Sets the commute user scale factor
        :param new_commute_user_scale_factor: The new scale factor as an int
        """
        self._commute_user_scale_factor = new_commute_user_scale_factor

    @property
    def approx_commute_range(self):
        """
        Approx commute range is the +/- of the acceptable commute range
        Therefore it the user desires 40-80 min commute, if the approx_commute range is 20,
        then the range becomes 20-100 minutes. This is due to the approximations of zip codes.
        Approx_commute_range is stored as minutes
        :return: The approx_commute_range in minutes
        """
        return self._approx_commute_range_minutes

    @approx_commute_range.setter
    def approx_commute_range(self, new_approx_commute_range_minutes):
        """
        Set the approx_commute range in minutes
        :param new_approx_commute_range_minutes:
        :return:
        """
        if new_approx_commute_range_minutes < 0:
            print("Error: Approx commute range less than zero")
            print("Setting to zero")
            self._approx_commute_range_minutes = 0
        else:
            self._approx_commute_range_minutes = new_approx_commute_range_minutes

    @property
    def max_user_commute(self):
        """
        Get the max_user_commute as minutes.
        This is the maximum commute that a user is willing to have
        :return: The max commute time in minutes
        """
        return self._max_user_commute_minutes

    @max_user_commute.setter
    def max_user_commute(self, new_max_user_commute_minutes):
        """
        Sets the max_user_commute as minutes
        :param new_max_user_commute_minutes: The new max_commute_time in minutes
        """
        self._max_user_commute_minutes = new_max_user_commute_minutes

    @property
    def min_user_commute(self):
        """
        Get the min_user_commute as minutes
        This is the minimum commute that uesr is willing to have
        :return: The min commute time in minutes
        """
        return self._min_user_commute_minutes

    @min_user_commute.setter
    def min_user_commute(self, new_min_user_commute):
        """
        Set the min_user_commute as minutes
        :param new_min_user_commute: The new min commute time as minutes
        """
        self._min_user_commute_minutes = new_min_user_commute

    def compute_approximate_commute_filter(self, approx_commute_times):
        """
        Returns whether or not the approximate commute times are within the
        user acceptable range. If any of the commutes are not within the acceptable
        range, then False is returned
        :param approx_commute_times: Must be a list of ints that correspond to the commute times.
            Currently the approx commute is done in minutes, i.e [20, 40 , 56]
        :return: True if the home is inside the range, False otherwise
        """
        for commute in approx_commute_times:
            if (commute > self.max_user_commute + self.approx_commute_range) \
                            or (commute < self.min_user_commute - self.approx_commute_range):
                return False
        return True

    def compute_commute_score(self, commute_minutes):
        """
        Compute the score based off the commute. A percent value of the fit of the home is returned.
        I.E, .67, .47, etc will be returned. The scaling will be done in the parent class
        Note: Since the eliminating filter should have been done first, this computation
            does not mark any home for elimination
        :param commute_minutes: The commute time in minutes.
        :return: THe percent fit the home is or -1 if the home should be eliminated
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
