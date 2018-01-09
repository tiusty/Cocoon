from houseDatabase.models import ZipCodeDictionaryParentModel, ZipCodeDictionaryChildModel

class HomeScore(object):
    # noinspection SpellCheckingInspection
    """
        Class stores a home with supporting information regarding the home. Keeps track of data
            while the algorithm is being computed

          Attributes:
            self._home (housedata.model): The actual home specified from the house database models.
            self._accumulated_points (int): The total amount of points this home has earned
            self._total_possible_points (int): The total amount of points this home could have earned
            self._approx_commute_times_minutes (dict{'(survey.model.destinations)', (int)}: A dictionary with the key being
                the destination and the value is the approximate commute time to that destination in minutes
            self._exact_commute_times_minutes (dict{'(survey.model.destinations)', (int)}: A dictionary with the key being
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
        """
        Takes in a dictionary of commutes and adds the ones that do not exist
            to the member dictionary
        :param new_approx_commute_time (dict{Destination: (int)}): Dictionary of Destinations and commute times in
            in minutes to be added to the home
        """
        self._approx_commute_times_minutes.update(new_approx_commute_time)

    @property
    def exact_commute_times(self):
        return self._exact_commute_times_minutes

    @exact_commute_times.setter
    def exact_commute_times(self, new_exact_commute_time):
        """
        Takes in a dictionary of commutes and adds the ones that do not exist
            to the member dictionary
        :param new_approx_commute_time (dict{Destination: (int)}): Dictionary of Destinations and commute times in
            in minutes to be added to the home
        """
        self._exact_commute_times_minutes.update(new_exact_commute_time)

    # TODO: Move to rent_algorithm (?)
    # This should probably be moved into the rent_algorithm file as a helper method, as it doesn't
    # actually interact with the object in any meaningful way.
    def calculate_approx_commute(self, origin_zip, destination, commute_type):
        """
        Computes an approximate commute time for this house to an input destination. First checks
        the zipcode database to see if the commute time is already stored; if it's not, it then
        returns the pair of failed zips, along with an error code as a 3 element list. The first
        entry of the list is 0 if the pair was in the database, and 1 if the pair wasn't in the database
        or if the pair wasn't valid. The last 2 entries are the origin and destination zip respectively.
        :param origin_zip: The home's zip code, eg. "12345"
        :param destination: The destination as a RentingDestinationsModel object
        :param commute_type: commute_type enum, eg. "Driving"
        :return True on success, False on failure.
        """
        parent_zip_code_dictionary = ZipCodeDictionaryParentModel.objects.filter(zip_code_parent__exact=origin_zip)
        if parent_zip_code_dictionary.exists():
            for parent in parent_zip_code_dictionary:
                zip_code_dictionary = ZipCodeDictionaryChildModel.objects.filter(
                    parent_zip_code_child_id=parent).filter(zip_code_child__exact=destination.zip_code)\
                    .filter(commute_type_child__exact=commute_type)
                if zip_code_dictionary.exists():
                    for match in zip_code_dictionary:
                        if match.zip_code_cache_still_valid():
                            self.approx_commute_times[destination.destination_key] = match.commute_time_minutes
                            return True
                        else:
                            return False
                else:
                    return False
        else:
            return False

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
