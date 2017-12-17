class ApproximateCommutes(object):

    def __init__(self):
        self._approx_commute_times = []
        self._approx_commute_range = 0
        self._max_user_commute = 0
        self
        # Need super to allow calling each classes constructor
        super(ApproximateCommutes, self).__init__()

    @property
    def approx_commute_times(self):
        """
        Returns the list of approximate commute times
        Approximate commute times stored as minutes
        :return: List of approximate times i.e (27, 27, 27)
        """
        return self._approx_commute_times

    @approx_commute_times.setter
    def approx_commute_times(self, new_approx_commute):
        """
        Appends a new approximate time to the list
        Times should be added as minutes
        :param new_approx_commute: Commute time in minutes
        """
        self._approx_commute_times.append(new_approx_commute)

    def compute_approximate_commute_score(self, min_user_commute, max_user_commute,
                                          approx_commute_range):
        for commute in self.approx_commute_times:
            if (commute >= max_user_commute + approx_commute_range) \
                            or (commute <= min_user_commute - approx_commute_range):
                return True
