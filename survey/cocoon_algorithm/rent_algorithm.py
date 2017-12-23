# Import survey modules
from survey.cocoon_algorithm.commute_algorithms import CommuteAlgorithm
from survey.cocoon_algorithm.price_algorithm import PriceAlgorithm
from survey.cocoon_algorithm.base_algorithm import CocoonAlgorithm
from survey.cocoon_algorithm.weighted_scoring_algorithm import WeightScoringAlgorithm
from survey.cocoon_algorithm.sorting_algorithms import SortingAlgorithms


class RentAlgorithm(SortingAlgorithms, WeightScoringAlgorithm, PriceAlgorithm, CommuteAlgorithm, CocoonAlgorithm):

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
            for commute in home_data.approx_commute_times:
                score_result = self.compute_commute_score(commute)
                home_data.accumulated_points = score_result * self.commute_user_scale_factor * self.commute_question_weight
                home_data.total_possible_points = self.commute_user_scale_factor * self.commute_question_weight

    def run_compute_price_score(self):
        """
        Runs the price scoring which will generate a score based on the price of the home. If the home
        returns a -1 for the score then the home is also marked for deletion
        """
        for home_data in self.homes:
            score_result = self.compute_price_score(home_data.home.get_price())
            if score_result == -1:
                home_data.eliminate_home()
            home_data.accumulated_points = score_result * self.price_user_scale_factor * self.price_question_weight
            home_data.total_possible_points = self.price_user_scale_factor * self.price_question_weight

    def run_compute_weighted_score_interior_amenities(self, air_conditioning_scale, washer_dryer_in_home_scale, dish_washer_scale, bath_scale):
        """
        Runs the interior amenities scoring.
        TODO Think of better way to run this function since it is kinda messy
        :param air_conditioning_scale: Int -> User scale for air_conditioning
        :param washer_dryer_in_home_scale: Int -> User scale for washer/dryer in home
        :param dish_washer_scale: Int -> User scale for dish washer
        :param bath_scale: Int -> User scale for bath
        """
        for home_data in self.homes:
            if self.compute_weighted_question_filter(air_conditioning_scale, home_data.home.get_air_conditioning()):
                home_data.eliminate_home()
            home_data.accumulated_points = self.compute_weighted_question_score(air_conditioning_scale,
                                                                                home_data.home.get_air_conditioning())
            home_data.total_possible_points = abs(air_conditioning_scale) * self.hybrid_question_weight

            if self.compute_weighted_question_filter(washer_dryer_in_home_scale, home_data.home.get_wash_dryer_in_home()):
                home_data.eliminate_home()

            home_data.accumulated_points = self.compute_weighted_question_score(washer_dryer_in_home_scale,
                                                                                home_data.home.get_wash_dryer_in_home())
            home_data.total_possible_points = abs(washer_dryer_in_home_scale) * self.hybrid_question_weight

            if self.compute_weighted_question_filter(dish_washer_scale, home_data.home.get_dish_washer()):
                home_data.eliminate_home()

            home_data.accumulated_points = self.compute_weighted_question_score(dish_washer_scale,
                                                                                home_data.home.get_dish_washer())
            home_data.total_possible_points = abs(dish_washer_scale) * self.hybrid_question_weight

            if self.compute_weighted_question_filter(bath_scale, home_data.home.get_bath()):
                home_data.eliminate_home()

            home_data.accumulated_points = self.compute_weighted_question_score(bath_scale, home_data.home.get_bath())
            home_data.total_possible_points = abs(bath_scale) * self.hybrid_question_weight

    def run_sort_home_by_score(self):
        """
        Sorts the homes by score. Will sort the homes list and return the homes reordered from left to right,
        best home to worst
        """
        self.homes = self.insertion_sort(self.homes)
