class SortingAlgorithms(object):
    """
    Class contains different sorting algorithms.
    """

    @staticmethod
    def insertion_sort(scored_homes):
        """
        Given a list of HomeScores classes. This will return the list with the homes
        ordered by score. The best match will be on the left. If two homes have equal percentages
        the home with the higher total_possible_points will be moved to the left (aka better scored)
        :param scored_homes: (List(HomeScore)): All the HomeScore objects for that survey
        :return: (List(HomeScore)): List of HomeScore classes ordered from left to right based off score
        """
        for index in range(1, len(scored_homes)):
            current_value = scored_homes[index]
            position = index

            while position > 0 and scored_homes[position - 1].percent_score() <= current_value.percent_score():
                if scored_homes[position - 1].percent_score() == current_value.percent_score() \
                        and scored_homes[position - 1].total_possible_points >= current_value.total_possible_points:
                    break
                scored_homes[position] = scored_homes[position - 1]
                position -= 1

            scored_homes[position] = current_value

        return scored_homes

    @staticmethod
    def run_sort_based_on_num_missing_amenities(scored_homes):
        """
        Runs insertion sort on each range of homes. Therefore homes with all the amenities are always first,
            then homes with decreasing number of amenities are shown.
        :param scored_homes: (List(HomeScore)): All the HomeScore objects for that survey
        :return: (List(HomeScore)): List of HomeScore classes ordered from left to right based off score
        """

        # First determine what the largest number of missing amenities are
        home_list = []
        largest_missing_num = 0
        for home in scored_homes:
            if len(home.missing_amenities) > largest_missing_num:
                largest_missing_num = len(home.missing_amenities)

        # Then split homes by number of amenities missing and sort each sub list
        #   Then homes that are missing less amenities go to the front of the list
        for num_missing in range(0, largest_missing_num+1):
            list_range = list(filter(lambda x: len(x.missing_amenities) == num_missing, scored_homes))
            home_list += SortingAlgorithms.insertion_sort(list_range)
