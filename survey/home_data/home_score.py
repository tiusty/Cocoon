from houseDatabase.models import ZipCodeDictionaryParentModel, ZipCodeDictionaryChildModel

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
        # If the setter is a list then set instead of append
        if isinstance(new_approx_commute_time, list):
            self._approx_commute_times_minutes = new_approx_commute_time
        else:
            self._approx_commute_times_minutes.append(new_approx_commute_time)


    def calculate_approx_commute(self, origin_zip, destination_zip, commute_type):
        """
        Computes an approximate commute time for this house to an input destination. First checks
        the zipcode database to see if the commute time is already stored; if it's not, it then
        returns the pair of failed zips, along with an error code as a 3 element list. The first
        entry of the list is 0 if the pair was in the database, and 1 if the pair wasn't in the database
        or if the pair wasn't valid. The last 2 entries are the origin and destination zip respectively.
        :param origin_zip: The home's zip code, eg. "12345"
        :param destination_zip: The destination's zip code, eg. "12345"
        :param commute_type: commute_type enum, eg. "Driving"
        :return A 3 element list containing the result, and the zip code pair. The result will be
            0 on successful lookup, 1 if parent not in database, 2 if child not in database, and 3
            if database cache is invalid.
        """
        print(ZipCodeDictionaryParentModel.objects.all())
        print(ZipCodeDictionaryChildModel.objects.all())
        parent_zip_code_dictionary = ZipCodeDictionaryParentModel.objects.filter(zip_code_parent__exact=origin_zip)
        if parent_zip_code_dictionary.exists():
            for parent in parent_zip_code_dictionary:
                zip_code_dictionary = ZipCodeDictionaryChildModel.objects.filter(
                    parent_zip_code_child_id=parent).filter(zip_code_child__exact=destination_zip)
                print(zip_code_dictionary)
                if zip_code_dictionary.exists():
                    for match in zip_code_dictionary:
                        if match.zip_code_cache_still_valid():
                            self.approx_commute_times = match.commute_time_minutes
                            return [0, origin_zip, destination_zip]
                        else:
                            return [3, origin_zip, destination_zip]
                else:
                    return [2, origin_zip, destination_zip]
        else:
            return [1, origin_zip, destination_zip]

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
                  + ") or _accumulated_points (" + str(self.accumulated_points) + ") is less than 0")
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
