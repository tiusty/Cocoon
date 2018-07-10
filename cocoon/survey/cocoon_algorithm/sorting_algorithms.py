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
