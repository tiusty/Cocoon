# Import global settings
from cocoon.survey.cocoon_algorithm.base_algorithm import CocoonAlgorithm

# Import survey modules
from cocoon.survey.cocoon_algorithm.commute_algorithms import CommuteAlgorithm
from cocoon.survey.cocoon_algorithm.price_algorithm import PriceAlgorithm
from cocoon.survey.cocoon_algorithm.sorting_algorithms import SortingAlgorithms
from cocoon.survey.cocoon_algorithm.weighted_scoring_algorithm import WeightScoringAlgorithm
from ..constants import NUMBER_OF_EXACT_COMMUTES_COMPUTED

# Import Commutes modules
from cocoon.commutes.models import ZipCodeBase, ZipCodeChild, CommuteType

# Import DistanceWrapper
from cocoon.commutes.distance_matrix.distance_wrapper import Distance_Matrix_Exception
from cocoon.commutes.distance_matrix import commute_cache_updater
from cocoon.commutes.distance_matrix.commute_retriever import retrieve_exact_commute_rent_algorithm

# Import Constants from commute module
from cocoon.commutes.constants import CommuteAccuracy
from cocoon.survey.constants import AVERAGE_BICYCLING_SPEED, AVERAGE_WALKING_SPEED, EXTRA_DISTANCE_LAT_LNG_APPROX

# Import Geolocator
import geopy.distance
import cocoon.houseDatabase.maps_requester as geolocator
from config.settings.Global_Config import gmaps_api_key


class RentAlgorithm(SortingAlgorithms, WeightScoringAlgorithm, PriceAlgorithm, CommuteAlgorithm, CocoonAlgorithm):
    """
    The rent algorithm class that contains all the helper functions to integrate all the different algorithm classes
    This class inherits a lot of variables and methods to support the functionality that it needs.
    """

    def populate_with_survey_information(self, user_survey):
        """
        Populates the rent algorithm member variables based on the survey values
        :param user_survey: (RentingSurveyModel): The survey the user filled out
        """
        # First populate homes
        self.populate_survey_homes(user_survey)

        # Populate the destinations in commute information
        self.populate_commute_algorithm(user_survey)

        # Second populate with the rest of survey information
        self.populate_price_algorithm_information(user_survey.price_weight, user_survey.max_price,
                                                  user_survey.desired_price, user_survey.min_price)

    def run_compute_approximate_commute_filter(self):
        """
        Runs the approximate commute filter which will eliminate homes outside
        of the users commute radius
        """
        for home_data in self.homes:
            if not self.approximate_commute_filter(home_data.approx_commute_times):
                home_data.eliminate_home()

    def run_compute_commute_score_approximate(self):
        """
        Runs the approximate commute scoring which will generate a score based on the approximate commute time.
        No homes will be marked for elimination since the filter should have already marked them
        """
        for home_data in self.homes:
            for commuter in home_data.approx_commute_times:
                score_result = self.compute_commute_score(home_data.approx_commute_times[commuter], commuter)
                home_data.accumulated_points = score_result * commuter.commute_weight \
                    * self.commute_question_weight
                home_data.total_possible_points = commuter.commute_weight * self.commute_question_weight

    def run_compute_commute_score_exact(self):
        """
        Runs the exact commute scoring on any homes that have exact commutes populated. Homes are never marked for
        deletion, it will only score based on a more accurate number
        :return:
        """
        for home_data in self.homes:
            for commuter in home_data.exact_commute_times:
                score_result = self.compute_commute_score(home_data.exact_commute_times[commuter], commuter)
                home_data.accumulated_points = score_result * commuter.commute_weight \
                    * self.commute_question_weight
                home_data.total_possible_points = commuter.commute_weight * self.commute_question_weight

    def retrieve_all_approximate_commutes(self):
        """
        First the function updates all the caches for the new homes and destinations. Then it will populate the rent
            algorithm with valid commutes
        """
        commute_cache_updater.update_commutes_cache_rent_algorithm(self.homes, self.tenants, accuracy=CommuteAccuracy.APPROXIMATE)
        for destination in self.tenants:
            lat_lng = ""

            # If the commute type is walking or bicycling then we need to generate a lat and lng for the destination
            # We do it here so we can save the lat and lng for every home
            if destination.commute_type.commute_type == CommuteType.BICYCLING or \
                    destination.commute_type.commute_type == CommuteType.WALKING:
                # Pulls lat/lon based on address
                lat_lng_result = geolocator.maps_requester(gmaps_api_key).\
                    get_lat_lon_from_address(destination.full_address)

                if lat_lng_result == -1:
                    continue
                else:
                    lat_lng = (lat_lng_result[0], lat_lng_result[1])

            self.populate_approx_commutes(self.homes, destination, lat_lng_dest=lat_lng)

    def populate_approx_commutes(self, homes, destination, lat_lng_dest=""):
        """
        Based on the commute type of the destination, this function determines the algorithm method that will
            be used to generate the approximation
        :param homes: (list[HomeScore]) -> The homes that the user is computing for
        :param destination: (DestinationModel): The destination as a RentingDestinationsModel object
        :param lat_lng_dest: ((decimal, decimal)): -> A Tuple of (latitude, longitude) for the destination
        """
        if destination.commute_type.commute_type == CommuteType.DRIVING:
            self.zip_code_approximation(homes, destination)
        elif destination.commute_type.commute_type == CommuteType.TRANSIT:
            self.zip_code_approximation(homes, destination)
        elif destination.commute_type.commute_type == CommuteType.BICYCLING:
            self.lat_lng_approximation(homes, destination, lat_lng_dest, AVERAGE_BICYCLING_SPEED)
        elif destination.commute_type.commute_type == CommuteType.WALKING:
            self.lat_lng_approximation(homes, destination, lat_lng_dest, AVERAGE_WALKING_SPEED)

    @staticmethod
    def lat_lng_approximation(homes, destination, lat_lng_dest, average_speed):
        """
        This function given a home and a destination will determine the distance between the two homes based off of the
            lat and lng points. Then once the distance is determined, then the commute time is determined based off of
            the average speed.
        :param homes: (list[homeScore]) -> The home that the user is computing for
        :param destination: (DestinationModel): The destination as a RentingDestinationsModel object
        :param lat_lng_dest: ((decimal, decimal)): -> A Tuple of (latitude, longitude) for the destination
        :param average_speed: (int) -> The average speed in mph that the person moves for the given mode of transport
        :return: (Boolean): -> True: The home approximation was found and added
                               False: The home was not able to have a approximation created
        """

        for home in homes:
            # Stores the lat and lng points for the home
            lat_lng_home = (home.home.latitude, home.home.longitude)

            # Returns the distance from the two lat lng points in miles
            distance = geopy.distance.geodesic(lat_lng_home, lat_lng_dest).miles

            # If the distance is less than a mile then don't add any distance since it is already so close
            if distance > 1:
                # Extra distance is determined by giving more distance to homes farther away
                extra_distance = EXTRA_DISTANCE_LAT_LNG_APPROX * (1 - 1.0/distance)
                # This normalizes the value since walking needs less of a weight than biking since homes
                #   are more direct when walking.
                distance += extra_distance * average_speed/AVERAGE_BICYCLING_SPEED
            if average_speed is not 0:
                # If the speed is not zero (to prevent divide by zero, then add the commute time to
                #   the home
                commute_time_hours = distance / average_speed
                commute_time = commute_time_hours * 60
                home.approx_commute_times[destination] = commute_time
            else:
                # If there was a divide by zero then just eliminate the home
                home.eliminate_home()

    @staticmethod
    def zip_code_approximation(homes, destination):
        """
        This is the zip_code_approximation algorithm. This assumes that the zip-code cache is already updated
            and that all the valid pairs are already generated. This just goes through and finds the valid pairs
            for the given zip_code and the destination
        :param homes: (list(HomeScore) -> The homes that the user is computing for
        :param destination: (DestinationModel): The destination as a RentingDestinationsModel object
        """

        try:
            # Retrieve the destination zip_code object if it exists
            destination_zip = ZipCodeBase.objects.get(zip_code=destination.zip_code)

            # Retrieve all the child zip_codes for the destination commute_type
            child_zips = ZipCodeChild.objects.filter(base_zip_code=destination_zip). \
                filter(commute_type=destination.commute_type). \
                values_list('zip_code', 'commute_time_seconds')

            # Dictionary Compression to retrieve the values from the QuerySet
            child_zip_codes = {zip_code: commute_time_seconds for zip_code, commute_time_seconds in child_zips}

            # For every home check to see if a zip code pair exists and then store the commute time
            for home in homes:

                # Determines if the home exists in the dictionary on child_zip_codes
                result = home.home.zip_code in child_zip_codes

                # If there was a match, (there should only be one)
                if result:
                    # Store the commute time associated with the zip_code
                    home.approx_commute_times[destination] = child_zip_codes[home.home.zip_code]/60
                else:
                    # If no result was returned, i.e the zip_code pair doesn't exist, then just eliminate the home
                    home.eliminate_home()

        # If the ZipCodeBase doesn't exist then... just don't compute, it should be there if the update_cache function
        # is called before this
        except ZipCodeBase.DoesNotExist:
            pass

    def retrieve_exact_commutes(self):
        """
        updates the exact_commute_minutes property for the top homes, based on a global variable
        in Global_Config. Uses the distance_matrix wrapper.
        """
        for destination in self.tenants:
            try:
                results = retrieve_exact_commute_rent_algorithm(self.homes[:NUMBER_OF_EXACT_COMMUTES_COMPUTED],
                                                                destination,
                                                                destination.commute_type,
                                                                with_traffic=destination.traffic_option)

                # Store the results to the homes
                for i in range(len(results)):
                    duration_seconds = results[i][0][0]
                    distance_meters = results[i][0][1]
                    if duration_seconds is not None and distance_meters is not None:
                        self.homes[i].exact_commute_times[destination] = int(duration_seconds / 60)

            except Distance_Matrix_Exception as e:
                print("Caught: " + e.__class__.__name__)

    def run_compute_price_score(self):
        """
        Runs the price scoring which will generate a score based on the price of the home. If the home
        returns a -1 for the score then the home is also marked for deletion
        """
        for home_data in self.homes:
            score_result = self.compute_price_score(home_data.home.price)
            if score_result == -1:
                home_data.eliminate_home()
            home_data.accumulated_points = score_result * self.price_user_scale_factor * self.price_question_weight
            home_data.total_possible_points = self.price_user_scale_factor * self.price_question_weight

    def run_compute_weighted_questions(self, survey):
        """
        Runs all the weighted questions associated with the survey

        All the homes are updated with the new score
        :param survey: (RentingSurvey Model) -> The survey the user took
        """
        for home_score in self.homes:
            self.run_compute_weighted_score_interior_amenities(survey, home_score)
            self.run_compute_weighted_score_exterior_amenities(survey, home_score)
            self.handle_laundry_weight_question(survey, home_score)

    def run_compute_weighted_score_interior_amenities(self, survey, home_score):
        """
        Runs the interior amenities scoring
        :param survey: (RentingSurvey Model) -> The survey the user took
        :param home_score: (HomeScore) -> The home that is currently being calaculated
        """
        if survey.wants_furnished:
            self.handle_weighted_question('home_furnished', survey.furnished_weight, home_score, home_score.home.furnished)
        if survey.wants_hardwood_floors:
            self.handle_weighted_question('hardwood_floors', survey.hardwood_floors_weight, home_score, home_score.home.hardwood_floors)
        if survey.wants_AC:
            self.handle_weighted_question('air_conditioning', survey.AC_weight, home_score, home_score.home.air_conditioning)
        if survey.wants_dishwasher:
            self.handle_weighted_question('dishwasher', survey.dishwasher_weight, home_score, home_score.home.dishwasher)

    def run_compute_weighted_score_exterior_amenities(self, survey, home_score):
        """
        Runs the exterior amenities scoring.
        :param survey: (RentingSurvey Model) -> The survey the user took
        :param home_score: (HomeScore) -> The home that is currently being calaculated
        """
        if survey.wants_patio:
            self.handle_weighted_question('patio_balcony', survey.patio_weight, home_score, home_score.home.patio_balcony)
        if survey.wants_pool:
            self.handle_weighted_question('pool', survey.pool_weight, home_score, home_score.home.pool)
        if survey.wants_gym:
            self.handle_weighted_question('gym', survey.gym_weight, home_score, home_score.home.gym)
        if survey.wants_storage:
            self.handle_weighted_question('storage', survey.storage_weight, home_score, home_score.home.storage)

    def run_sort_home_by_score(self):
        """
        Sorts the homes by score. Will sort the homes list and return the homes reordered from left to right,
        best home to worst
        """
        self.homes = self.insertion_sort(self.homes)

    def run(self, survey):
        """
        STEP 1: Populate the rent_algorithm with all the information from the survey
        """
        self.populate_with_survey_information(survey)

        """
        STEP 2: Compute the approximate distance using zip codes from the possible homes and the desired destinations.
        This also will store how long the commute will take which will be used later for Dynamic filtering/scoring
        """
        self.retrieve_all_approximate_commutes()

        """
        STEP 3: Remove homes that are too far away using approximate commutes
        """
        self.run_compute_approximate_commute_filter()

        """
        STEP 4: Generate scores based on hybrid questions
        """
        self.run_compute_commute_score_approximate()
        self.run_compute_price_score()
        self.run_compute_weighted_questions(survey)
        """
        STEP 5: Now sort all the homes from best homes to worst home
        """
        self.run_sort_home_by_score()

        """
        STEP 6: Compute the exact commute time/distance for best homes
        """
        self.retrieve_exact_commutes()

        """
        STEP 7: Score the top homes based on the exact commute time/distance
        """
        self.run_compute_commute_score_exact()

        """
        STEP 8: Reorder homes again now with the full data
        """
        # Now reorder all the homes with the new information
        self.run_sort_based_on_num_missing_amenities(self.homes)
