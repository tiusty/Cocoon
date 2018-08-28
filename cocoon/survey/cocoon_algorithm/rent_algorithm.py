# Import global settings
from config.settings.Global_Config import number_of_exact_commutes_computed
from cocoon.survey.cocoon_algorithm.base_algorithm import CocoonAlgorithm

# Import survey modules
from cocoon.survey.cocoon_algorithm.commute_algorithms import CommuteAlgorithm
from cocoon.survey.cocoon_algorithm.price_algorithm import PriceAlgorithm
from cocoon.survey.cocoon_algorithm.sorting_algorithms import SortingAlgorithms
from cocoon.survey.cocoon_algorithm.weighted_scoring_algorithm import WeightScoringAlgorithm

# Import DistanceWrapper
from cocoon.commutes.distance_matrix.distance_wrapper import DistanceWrapper, Distance_Matrix_Exception
from cocoon.commutes.distance_matrix.update_commutes_cache import update_commutes_cache

# Import Constants from commute module
from cocoon.commutes.constants import GoogleCommuteNaming, CommuteAccuracy


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
            if not self.compute_approximate_commute_filter(home_data.approx_commute_times):
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
        retrieves the commute time and distance between each origin and each destination (zip code) and updates
        the approx_commute_minutes dictionary within each HomeScore accordingly. For any zip code combinations that
        are not in the database, the distance matrix is called to calculate the approximate distance and the
        database is updated.
        """
        update_commutes_cache(self.homes, self.destinations, accuracy=CommuteAccuracy.APPROXIMATE)
        for destination in self.destinations:
            for home in self.homes:
                if not home.populate_approx_commutes(home.home.zip_code, destination):
                    home.eliminate_home()

    def retrieve_exact_commutes(self):
        """
        updates the exact_commute_minutes property for the top homes, based on a global variable
        in Global_Config. Uses the distance_matrix wrapper.
        """
        distance_matrix_requester = DistanceWrapper()

        for destination in self.destinations:
            try:
                # map list of HomeScore objects to full addresses
                origin_addresses = list(map(lambda house:house.home.full_address,
                                       self.homes[:number_of_exact_commutes_computed]))

                destination_address = destination.full_address

                results = distance_matrix_requester.get_durations_and_distances(origin_addresses,
                                                                                [destination_address],
                                                                                mode=destination.commute_type.commute_type)

                # iterates over min of number to be computed and length of results in case lens don't match
                for i in range(min(number_of_exact_commutes_computed, len(results))):
                    # update exact commute time with in minutes
                    self.homes[i].exact_commute_times[destination] = int(results[i][0][0] / 60)

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

    def run_compute_weighted_score_interior_amenities(self, air_conditioning_scale, washer_dryer_in_home_scale,
                                                      dish_washer_scale, bath_scale):
        """
        Runs the interior amenities scoring.
        # TODO Think of better way to run this function since it is kinda messy
        :param air_conditioning_scale: Int -> User scale for air_conditioning
        :param washer_dryer_in_home_scale: Int -> User scale for washer/dryer in home
        :param dish_washer_scale: Int -> User scale for dish washer
        :param bath_scale: Int -> User scale for bath
        """
        for home_data in self.homes:
            if not (self.compute_weighted_question_filter(air_conditioning_scale, home_data.home.air_conditioning)):
                home_data.eliminate_home()
            home_data.accumulated_points = self.compute_weighted_question_score(air_conditioning_scale,
                                                                                home_data.home.air_conditioning)
            home_data.total_possible_points = abs(air_conditioning_scale) * self.hybrid_question_weight

            if not (self.compute_weighted_question_filter(washer_dryer_in_home_scale, home_data.home.interior_washer_dryer)):
                home_data.eliminate_home()

            home_data.accumulated_points = self.compute_weighted_question_score(washer_dryer_in_home_scale,
                                                                                home_data.home.interior_washer_dryer)
            home_data.total_possible_points = abs(washer_dryer_in_home_scale) * self.hybrid_question_weight

            if not (self.compute_weighted_question_filter(dish_washer_scale, home_data.home.dish_washer)):
                home_data.eliminate_home()

            home_data.accumulated_points = self.compute_weighted_question_score(dish_washer_scale,
                                                                                home_data.home.dish_washer)
            home_data.total_possible_points = abs(dish_washer_scale) * self.hybrid_question_weight

            if not (self.compute_weighted_question_filter(bath_scale, home_data.home.bath)):
                home_data.eliminate_home()

            home_data.accumulated_points = self.compute_weighted_question_score(bath_scale, home_data.home.bath)
            home_data.total_possible_points = abs(bath_scale) * self.hybrid_question_weight

    def run_sort_home_by_score(self):
        """
        Sorts the homes by score. Will sort the homes list and return the homes reordered from left to right,
        best home to worst
        """
        self.homes = self.insertion_sort(self.homes)
