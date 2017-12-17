from survey.cocoon_algorithm.approximate_commutes_algorithm import ApproximateCommutes
from survey.cocoon_algorithm.base_algorithm import CocoonAlgorithm


class RentAlgorithm(ApproximateCommutes, CocoonAlgorithm):

    def run_compute_approximate_commute_score(self):
        """
        Runs the approximate commute algorithm which will eliminate homes outside
        of the users commute radius
        """
        for home in self.homes:
            if not self.compute_approximate_commute_score(home.approx_commute_times):
                home.eliminate_home()
