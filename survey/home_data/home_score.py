
class HomeScore(object):

    def __init__(self, new_house=None):
        self._house = new_house
        self._accumulated_points = 0
        self._total_possible_points = 0
        self._eliminated = False

    def percent_score(self):
        """
        Generates the score percentage
        :return:
        """
        if self._total_possible_points != 0 and self.eliminated is False:
            return (self._accumulated_points / self._total_possible_points) * 100
        elif self.eliminated:
            return -1
        else:
            return 0

    def user_friendly_score(self):
        """
        Produces a user friendly version of the percent score
        :return: The score percent rounded
        """
        return round(self.percent_score())

    @property
    def eliminated(self):
        return self._eliminated

    @eliminated.setter
    def eliminated(self, is_eliminated):
        self._eliminated = is_eliminated
