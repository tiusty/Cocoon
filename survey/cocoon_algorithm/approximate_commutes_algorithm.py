class ApproximateCommutes(object):

    def __init__(self):
        self._approx_commute_times_minutes = []
        self._approx_commute_range_minutes = 0
        self._max_user_commute_minutes = 0
        self._min_user_commute_minutes = 0
        # Need super to allow calling each classes constructor
        super(ApproximateCommutes, self).__init__()

    @property
    def approx_commute_times(self):
        """
        Returns the list of approximate commute times
        Approximate commute times stored as minutes
        :return: List of approximate times i.e (27, 27, 27)
        """
        return self._approx_commute_times_minutes

    @approx_commute_times.setter
    def approx_commute_times(self, new_approx_commute_minutes):
        """
        Appends a new approximate time to the list
        Times should be added as minutes
        :param new_approx_commute: Commute time in minutes
        """
        self._approx_commute_times_minutes.append(new_approx_commute_minutes)

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

    def compute_approximate_commute_score(self):
        """
        Returns whether or not the approximate commute times are within the
        user acceptable range. If any of the commutes are not within the acceptable
        range, then False is returned
        :return: True if the home is inside the range, False otherwise
        """
        for commute in self.approx_commute_times:
            if (commute >= self.max_user_commute + self.approx_commute_range) \
                            or (commute <= self.min_user_commute - self.approx_commute_range):
                return False
        return True
