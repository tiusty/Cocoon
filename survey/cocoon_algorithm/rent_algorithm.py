# Import Django modules
from django.db.models import Q

# Import global settings
from Unicorn.settings.Global_Config import number_of_exact_commutes_computed

# Import houseDatabase modules
from houseDatabase.models import RentDatabaseModel, HomeTypeModel

# Import survey modules
from survey.cocoon_algorithm.commute_algorithms import CommuteAlgorithm
from survey.cocoon_algorithm.price_algorithm import PriceAlgorithm
from survey.cocoon_algorithm.base_algorithm import CocoonAlgorithm
from survey.cocoon_algorithm.weighted_scoring_algorithm import WeightScoringAlgorithm
from survey.cocoon_algorithm.sorting_algorithms import SortingAlgorithms

# Import HomeScore class
from survey.home_data.home_score import HomeScore

# Import DistanceWrapper
from survey.distance_matrix.distance_wrapper import *
from survey.approximate_commute_handler import compute_approximates

import math

class RentAlgorithm(SortingAlgorithms, WeightScoringAlgorithm, PriceAlgorithm, CommuteAlgorithm, CocoonAlgorithm):

    def populate_survey_destinations_and_possible_homes(self, user_survey):

        # Find all the possible homes that fit the static filter
        filtered_home_list = self.generate_static_filter_home_list(user_survey)

        # Add homes to rent_algorithm
        for home in filtered_home_list:
            self.homes = HomeScore(home)

        # Retrieves all the destinations that the user recorded
        self.destinations = user_survey.rentingdestinationsmodel_set.all()

    @staticmethod
    def generate_static_filter_home_list(user_survey):
        """
        Compute Static Elements
        The item that will filter the list the most should be first to narrow down the number of iterations
        The database needs to be searched
        (Right now it isn't order by efficiency but instead by when it was added. Later it can be switched around

        Current order:
        1. Filter by price range. The House must be in the correct range to be accepted
        2. Filter by Home Type. The home must be the correct home type to be accepted
        3. Filter by Move In day. The two move in days create the range that is allowed. The range is inclusive
            If the house is outside the range it is eliminated
        4. Filter by the number of bed rooms. It must be the correct number of bed rooms to work.
        4. Filter by the number of bathrooms
        """

        # Find all the home types the user desires
        current_home_types = []
        for home in user_survey.home_type.all():
            current_home_types.append(home.home_type)

        # Create queries for all the user home types desired
        home_type_queries = [Q(home_type_home=value) for value in
                             HomeTypeModel.objects.filter(home_type_survey__in=current_home_types)]

        # Or all the home type queries together, to make one query
        query_home_type = home_type_queries.pop()
        for item in home_type_queries:
            query_home_type |= item

        # Query the database
        return RentDatabaseModel.objects \
            .filter(price_home__range=(user_survey.min_price, user_survey.max_price)) \
            .filter(query_home_type) \
            .filter(move_in_day_home__range=(user_survey.move_in_date_start, user_survey.move_in_date_end)) \
            .filter(num_bedrooms_home=user_survey.num_bedrooms) \
            .filter(num_bathrooms_home__range=(user_survey.min_bathrooms, user_survey.max_bathrooms))

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
                score_result = self.compute_commute_score(home_data.approx_commute_times[commute])
                home_data.accumulated_points = score_result * self.commute_user_scale_factor \
                    * self.commute_question_weight
                home_data.total_possible_points = self.commute_user_scale_factor * self.commute_question_weight

    def run_compute_commute_score_exact(self):
        """
        Runs the exact commute scoring on any homes that have exact commutes populated. Homes are never marked for
        deletion, it will only score based on a more accurate number
        :return:
        """
        for home_data in self.homes:
            for commute in home_data.exact_commute_times:
                score_result = self.compute_commute_score(home_data.exact_commute_times[commute])
                home_data.accumulated_points = score_result * self.commute_user_scale_factor \
                    * self.commute_question_weight
                home_data.total_possible_points = self.commute_user_scale_factor * self.commute_question_weight

    def retrieve_all_approximate_commutes(self):
        """
        retrieves the commute time and distance between each origin and each destination (zip code) and updates
        the approx_commute_minutes dictionary within each HomeScore accordingly. For any zip code combinations that
        are not in the database, the distance matrix is called to calculate the approximate distance and the
        database is updated.
        """

        # 1: Query DB and update when info is there
        failed_home_dict = dict()
        # destination will be a DestinationsModel object
        for destination in self.destinations:
            failed_list = []
            # home will be a HomeScore object
            for home in self.homes:
                in_database = home.calculate_approx_commute(home.home.zip_code, destination, "driving")
                # Case we have a match
                # code_and_distance is a 2 element list, first an error code and second the commute time in minutes
                if in_database != True:
                    failed_list.append((home.home.zip_code, home.home.state))
            # Add to the dictionary of failed homes
            failed_home_dict[(destination.zip_code, destination.state)] = failed_list

        # 2: Use approx handler to compute the failed home distances and update db
        for destination, origin_list in failed_home_dict.items():
            try:
                compute_approximates.approximate_compute_handler(origin_list, destination, "driving")
            except Distance_Matrix_Exception as e:
                print("Caught: " + e.__class__.__name__)

        # 3: Recompute failed homes using new DB data.

        for home in self.homes:
            if len(home.approx_commute_times) < len(self.destinations):
                # Recompute missing destinations
                for destination in self.destinations:
                    if destination.destination_key not in home.approx_commute_times:
                        new_in_database = home.calculate_approx_commute(home.home.zip_code, destination, "driving")
                        if new_in_database != True:
                            # Error: For some reason, the database was not updated, so we mark home for deletion
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

                results = distance_matrix_requester.calculate_distances(origin_addresses, [destination_address])

                for i in range(min(len(self.homes[:number_of_exact_commutes_computed]), len(results))):
                    # update exact commute time with in minutes
                    self.homes[i].exact_commute_times[destination.destination_key] = int(results[i][0][0] / 60)

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
        TODO Think of better way to run this function since it is kinda messy
        :param air_conditioning_scale: Int -> User scale for air_conditioning
        :param washer_dryer_in_home_scale: Int -> User scale for washer/dryer in home
        :param dish_washer_scale: Int -> User scale for dish washer
        :param bath_scale: Int -> User scale for bath
        """
        for home_data in self.homes:
            if self.compute_weighted_question_filter(air_conditioning_scale, home_data.home.air_conditioning):
                home_data.eliminate_home()
            home_data.accumulated_points = self.compute_weighted_question_score(air_conditioning_scale,
                                                                                home_data.home.air_conditioning)
            home_data.total_possible_points = abs(air_conditioning_scale) * self.hybrid_question_weight

            if self.compute_weighted_question_filter(washer_dryer_in_home_scale, home_data.home.interior_washer_dryer):
                home_data.eliminate_home()

            home_data.accumulated_points = self.compute_weighted_question_score(washer_dryer_in_home_scale,
                                                                                home_data.home.interior_washer_dryer)
            home_data.total_possible_points = abs(washer_dryer_in_home_scale) * self.hybrid_question_weight

            if self.compute_weighted_question_filter(dish_washer_scale, home_data.home.dish_washer):
                home_data.eliminate_home()

            home_data.accumulated_points = self.compute_weighted_question_score(dish_washer_scale,
                                                                                home_data.home.dish_washer)
            home_data.total_possible_points = abs(dish_washer_scale) * self.hybrid_question_weight

            if self.compute_weighted_question_filter(bath_scale, home_data.home.bath):
                home_data.eliminate_home()

            home_data.accumulated_points = self.compute_weighted_question_score(bath_scale, home_data.home.bath)
            home_data.total_possible_points = abs(bath_scale) * self.hybrid_question_weight

    def run_sort_home_by_score(self):
        """
        Sorts the homes by score. Will sort the homes list and return the homes reordered from left to right,
        best home to worst
        """
        self.homes = self.insertion_sort(self.homes)
