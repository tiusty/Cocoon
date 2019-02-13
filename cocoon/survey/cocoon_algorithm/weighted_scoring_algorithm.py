from ..constants import HYBRID_WEIGHT_MAX, HYBRID_WEIGHT_MIN, HYBRID_QUESTION_WEIGHT


class WeightScoringAlgorithm(object):
    """
    Class adds the weighted scoring functionality

      Attributes:
        self._hybrid_weight_global_min (int): The hybrid weight min from the global config file
        self._hybrid_weight_global_max (int): The hybrid weight max from the global config file
        self._hybrid_question_weight (int): The cocoon hybrid question weight from the global config file

    """

    def __init__(self):
        self.hybrid_weight_global_min = HYBRID_WEIGHT_MIN
        self.hybrid_weight_global_max = HYBRID_WEIGHT_MAX
        self.hybrid_question_weight = HYBRID_QUESTION_WEIGHT
        super(WeightScoringAlgorithm, self).__init__()

    def compute_weighted_question_filter(self, user_scale_factor, does_home_contain_item):
        """
        Returns whether the weighted question is going to eliminate the home
        :param user_scale_factor: (int): The user scale factor as an item
        :param does_home_contain_item: (Boolean): Boolean of whether or not the home as the item
        :return: (Boolean): True: The home is not eliminated, False: The home is eliminated
        """
        if user_scale_factor == self.hybrid_weight_global_max and does_home_contain_item is False:
            return False
        else:
            return True

    def compute_weighted_question_score(self, user_scale_factor, does_home_contain_item):
        """
        This function returns the score that home generates based off a hybrid weighted question
        :param user_scale_factor: (int): The user defined scale factor for the question
        :param does_home_contain_item: (Boolean): A boolean determining if the home contains the desired item
        :return: (int): An int ranging from negative (user_scale_factor * hybrid question weight) to positive
            (user_scale_factor * hybrid_question_weight)
        """
        return (1 if does_home_contain_item else 0) * user_scale_factor * self.hybrid_question_weight

    def handle_weighted_question_score(self, user_scale_factor, home, does_home_contain_item):
        """
        Handles the weighted question score based on a scale factor and the home
        :param user_scale_factor: (int) -> the user weight for that amenity
        :param home: (HomeScore) -> The home that is being judged
        :param does_home_contain_item: (Boolean): Boolean of whether or not the home as the item
        """
        home.accumulated_points = self.compute_weighted_question_score(user_scale_factor, does_home_contain_item)
        home.total_possible_points = abs(user_scale_factor) * self.hybrid_question_weight

    def handle_weighted_question(self, user_scale_factor, home, does_home_contain_item):
        """
        Handles weighted question scoring and filtering.
        Handles the weighted question score based on a scale factor and the home
        :param user_scale_factor: (int) -> the user weight for that amenity
        :param home: (HomeScore) -> The home that is being judged
        :param does_home_contain_item: (Boolean): Boolean of whether or not the home as the item
        """
        if not (self.compute_weighted_question_filter(user_scale_factor, does_home_contain_item)):
            home.eliminate_home()
        self.handle_weighted_question_score(user_scale_factor, home, does_home_contain_item)

    def handle_laundry_weight_question(self, survey, home_score):
        """
        Handles laundry weighting since it is a special case

        Basically:
            If the user wants in-unit then score based on in-unit
            If the user wants in-buliding then score homes with in-building normally but also score any apartment
                with in-unit laundry with the in-building scoring. This is assuming any person that wants in building
                laundry will also be good with in-unit. aka in-unit is the strictest case.
        :param survey: (RentingSurveyModel) -> The survey the user took
        :param home_score: (HomeScore) -> The home that is being evaluated
        """

        # Case if the user wants both laundry in-unit and in building
        if survey.wants_laundry_in_unit and survey.wants_laundry_in_building:

            # If the laundry is in-unit then just score the home based on having it in-unit
            if home_score.home.laundry_in_unit:
                self.handle_weighted_question(survey.laundry_in_unit_weight, home_score, home_score.home.laundry_in_unit)
            # If the home doesn't have it in-unit then score it for in-unit (going to be zero),
            #   then score it for having it in building
            else:
                self.handle_weighted_question(survey.laundry_in_unit_weight, home_score, home_score.home.laundry_in_unit)
                self.handle_weighted_question(survey.laundry_in_building_weight, home_score, home_score.home.laundry_in_building)

        # If the user just wants in-unit then score normally
        elif survey.wants_laundry_in_unit:
            self.handle_weighted_question(survey.laundry_in_unit_weight, home_score, home_score.home.laundry_in_unit)
        # If the user wants just in building then treat homes with in-unit has having the
        #   laundry in building (since it is "better")
        elif survey.wants_laundry_in_building:
            # If the home has in-unit laundry then score using the in-building weighting on the home
            #   though it is based off the fact that it has it in-unit
            if home_score.home.laundry_in_unit:
                self.handle_weighted_question(survey.laundry_in_building_weight, home_score, home_score.home.laundry_in_unit)
            else:
                self.handle_weighted_question(survey.laundry_in_building_weight, home_score, home_score.home.laundry_in_building)

