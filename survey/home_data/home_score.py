from houseDatabase.models import ZipCodeDictionaryParent, ZipCodeDictionaryChild

class HomeScore(object):

    def __init__(self, new_home=None):
        #Note: What kind of object is home? 
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

    """
    Uses GoogleMaps API to compute exact commute time from this house's address to an
    input destination address. If there is no commute time, this house is marked as 
    eliminated.
    Paramters: full_address - the home's full address
               destination - the destination's full address
               commute_type - the type of commute (eg. biking, transit)
    Returns: The exact commute time, in seconds, and the distance, in the given units, as a list.
    Only returns if there is not an error.
    """
    def calculate_exact_commute(self, full_address, destination, commute_type):
        #Are we still using Imperial, despite commute distances being in meters?
        measure_units = "metric"
        origins = []
        destinations = []
        origins.append(full_address)
        origins.append(destination)
        matrix = gmaps.distance_matrix(origins, destinations, mode=commute_type, units=measure_units)
        #Check for error in receiving matrix
        #TODO: Robust error checking
        if matrix:
            commute = matrix["rows"][0]["elements"]
            if commute['status'] == 'OK':
                return [commute['duration']["value"], commute['distance']["value"]]
            else:
                self.eliminated = True
        else:
            print("Error parsing API response")

    """
    Computes an approximate commute time for this house to an input destination. First checks
    the zipcode database to see if the commute time is already stored; if it's not, it then
    computes an exact commute time and adds this to the database.
    """
    def calculate_approx_commute(self, home_zip, home_address, destination_zip, destination_address, commute_type):
        #First check if already in the database
        zip_code_dictionary = ZipCodeDictionaryChild.objects.filter(_base_zip_code=home_zip, _zip_code=destination_zip)
        if zip_code_dictionary.exists():
            for match in zip_code_dictionary:
                if match.zip_code_cache_still_valid():
                    #TODO: Make this a dictionary, or include zips?
                    self.approx_commute_times = match.commute_time_minutes
                else:
                    #Not sure if this is correct at all, will review
                    match.commute_time_minutes = calculate_exact_commute(self, home_address, destination_address, commute_type)
        else: 
            #TODO: Error checking, is this even how we do the commute computation?
            if not ZipCodeDictionaryParent.objects.filter(_zip_code=home_zip).exists():
                ZipCodeDictionaryParent.objects.create(_zip_code=home_zip)
            #Create ZipCodeChildObject
            commute = calculate_exact_commute(self, home_address, destination_address, commute_type)
            ZipCodeDictionaryChild.objects.create(_zip_code=destination_zip,
                                                      _base_zip_code=home_zip,
                                                      _commute_time_seconds=commute[0],
                                                      _commute_distance_meters=commute[1],
                                                      _late_date_updated=timezone.now().date(),
                                                      _commute_type=commute_type,
                                                      )

    def percent_score(self):
        """
        Generates the score percentage
        :return:
        """
        if self.eliminated:
            return -1
        elif self._accumulated_points < 0 or self._total_possible_points < 0:
            print("Error: _total_possible_points (" + str(self._total_possible_points)
                  + ") or _accumulated_points (" + str(self._accumulated_points) + " are 0)")
            return -1
        elif self._total_possible_points != 0:
            return (self._accumulated_points / self._total_possible_points) * 100
        else:
            return 0

    def user_friendly_score(self):
        """
        Produces a user friendly version of the percent score
        :return: The score percent rounded
        """
        return round(self.percent_score())

