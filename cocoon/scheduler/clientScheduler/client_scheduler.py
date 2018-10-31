# import distance matrix wrapper
from cocoon.commutes.distance_matrix.distance_wrapper import DistanceWrapper
from cocoon.scheduler.clientScheduler.base_algorithm import clientSchedulerAlgorithm


class ClientScheduler(object):

    def __init__(self):
        self.algorithm = clientSchedulerAlgorithm()
        self.wrapper = DistanceWrapper()

    def build_homes_matrix(self, homes_list):
        """
        builds the homes matrix using the DistanceWrapper for now. Basically computes the distances using the Google Distance Matrix API and stores it.

        :param homes_list: List of strings containing home addresses used to compute the optimal itinerary
        :return: homes_matrix: a 2x2 matrix of distances found using the DistanceWrapper() to indicate the distances betweeen any two homes
        """

        homes_matrix = []

        for home_one in homes_list:

            home_one_distances = []

            result_distance_wrapper = self.wrapper.get_durations_and_distances(origins=[home_one],
                                                                               destinations=homes_list)

            for source, time in result_distance_wrapper[0]:
                home_one_distances.append(time)

            homes_matrix.append(home_one_distances)

        return homes_matrix

    def interpret_algorithm_output(self, homes_list, shortest_path):

        """
        Interprets the shortest path using the home list to make it ready for output onto the main site
    
        args:
        :param homes_list: The matrix calcualted using DistanceWrapper() with distances between every pair of homes in favorited list
        :param shortest_path: List of indices that denote the shortest path, which is the output of the algorithm
        :return: interpreted_route: List of strings containing the addresses in order of the shortest possible path, human readable
        """

        interepreted_route = []

        for item in shortest_path:
            interepreted_route.append(homes_list[item])

        return interepreted_route

    def run_client_scheduler_algorithm(self, homes_list):

        """
        Creates the home matrix and calls the calculation algorithm to find the shortest path
    
        args:
        :param homes_list: The matrix calcualted using DistanceWrapper() with distances between every pair of homes in favorited list
        :return: shortest_path: List of indices that denote the shortest path, which is the output of the algorithms
        """

        homes_matrix = self.build_homes_matrix(homes_list)
        shortest_path = self.algorithm.calculate_path(homes_matrix)

        return shortest_path
