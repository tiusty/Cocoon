
class HomeScore(object):

    def __init__(self, new_home=None):
        self._home = new_home
        self._accumulated_points = 0
        self._total_possible_points = 0
        self._approx_commute_times_minutes = []
        self._eliminated = False

    @property
    def eliminated(self):
        return self._eliminated

    @eliminated.setter
    def eliminated(self, is_eliminated):
        self._eliminated = is_eliminated

    def eliminate_home(self):
        self.eliminated = True

    @property
    def home(self):
        return self._home

    @home.setter
    def home(self, new_home):
        self._home = new_home

    @property
    def approx_commute_times(self):
        return self._approx_commute_times_minutes

    @approx_commute_times.setter
    def approx_commute_times(self, new_approx_commute_time):
        # TODO If the setter is a list then set instead of append
        self._approx_commute_times_minutes.append(new_approx_commute_time)

    @property
    def accumulated_points(self):
        return self._accumulated_points

    @accumulated_points.setter
    def accumulated_points(self, new_points):
        self._accumulated_points += new_points

    @property
    def total_possible_points(self):
        return self._total_possible_points

    @total_possible_points.setter
    def total_possible_points(self, new_possible_points):
        self._total_possible_points += new_possible_points

    def percent_score(self):
        """
        Generates the score percentage
        :return:
        """
        if self.eliminated:
            return -1
        elif self.accumulated_points < 0 or self.total_possible_points < 0:
            print("Error: _total_possible_points (" + str(self.total_possible_points)
                  + ") or _accumulated_points (" + str(self.accumulated_points) + " are 0)")
            return -1
        elif self.total_possible_points != 0:
            return (self.accumulated_points / self.total_possible_points) * 100
        else:
            return 0

    def user_friendly_score(self):
        """
        Produces a user friendly version of the percent score
        :return: The score percent rounded
        """
        return round(self.percent_score())

