from survey.cocoon_algorithm.approximate_commutes_algorithm import ApproximateCommutes
from survey.cocoon_algorithm.price_algorithm import PriceAlgorithm
from survey.cocoon_algorithm.base_algorithm import CocoonAlgorithm


class RentAlgorithm(PriceAlgorithm, ApproximateCommutes, CocoonAlgorithm):

    def run_compute_approximate_commute_score(self):
        """
        Runs the approximate commute algorithm which will eliminate homes outside
        of the users commute radius
        """
        for home in self.homes:
            if not self.compute_approximate_commute_score(home.approx_commute_times):
                home.eliminate_home()

    def run_compute_price_score(self):
        for home_data in self.homes:
            score_result = self.compute_price_score(home_data.home.get_price())
            if score_result == -1:
                home_data.eliminate_home()
            home_data.accumulated_points = score_result * self.price_user_scale_factor * self.price_question_weight
            home_data.total_possible_points = self.price_user_scale_factor * self.price_question_weight
