# import python modules

from datetime import datetime
import os


# import distance matrix wrapper
from cocoon.commutes.distance_matrix.commute_retriever import retrieve_exact_commute
from cocoon.scheduler.clientScheduler.base_algorithm import clientSchedulerAlgorithm
from cocoon.scheduler.models import ItineraryModel, itinerary_directory_path

# import django modules
from django.core.files.base import ContentFile
from cocoon.commutes.models import CommuteType

class ClientScheduler(clientSchedulerAlgorithm):


    def build_homes_matrix(self, homes_list):
        """
        builds the homes matrix using the DistanceWrapper for now. Basically computes the distances using the Google Distance Matrix API and stores it.

        :param (list) homes_list: List of strings containing home addresses used to compute the optimal itinerary
        :return: (list): homes_matrix a nxn matrix of distances found using the DistanceWrapper() to indicate the distances betweeen any two homes
        """

        homes_matrix = []

        for home_one in homes_list:

            home_one_distances = []
            commute_type = CommuteType.objects.get_or_create(commute_type=CommuteType.DRIVING)[0]
            result_distance_wrapper = retrieve_exact_commute([home_one], homes_list, commute_type)
            for source, time in result_distance_wrapper[0]:
                home_one_distances.append(time)

            homes_matrix.append(home_one_distances)

        return homes_matrix

    def interpret_algorithm_output(self, homes_list, shortest_path):

        """
        Interprets the shortest path using the home list to make it ready for output onto the main site
        args:
        :param (list) homes_list: The matrix calcualted using DistanceWrapper() with distances between every pair of homes in favorited list
        :param (list) shortest_path: List of indices that denote the shortest path, which is the output of the algorithm
        :return: (list): interpreted_route List of strings containing the addresses in order of the shortest possible path, human readable
        """

        interepreted_route = []

        for item in shortest_path:

            interepreted_route.append((homes_list[item[0]], item[1]))

        return interepreted_route

    def run_client_scheduler_algorithm(self, homes_list):

        """
        Creates the home matrix and calls the calculation algorithm to find the shortest path
        args:
        :param homes_list: The matrix calcualted using DistanceWrapper() with distances between every pair of homes in favorited list
        :return: (list): shortest_path List of indices that denote the shortest path, which is the output of the algorithms
        """

        homes_matrix = self.build_homes_matrix(homes_list)
        shortest_path = self.calculate_path(homes_matrix)
        edge_weights = self.get_edge_weights()

        tuple_list_edges = []

        for i in range(len(shortest_path)):
            temp_tuple = (shortest_path[i], edge_weights[i])
            tuple_list_edges.append(temp_tuple)

        return tuple_list_edges

    def run(self, homes_list, user):
        """
        Algorithm runner
        args:
        :param: (list) homes_list: The matrix calcualted using DistanceWrapper() with distances between every pair of homes in favorited list
        :param: (request.user) user: user
        """

        if not ItineraryModel.objects.filter(client=user).exists():
            destination_addresses = []
            for item in homes_list:
                destination_addresses.append(item.full_address)

            shortest_path = self.run_client_scheduler_algorithm(destination_addresses)
            interpreted_route = self.interpret_algorithm_output(destination_addresses, shortest_path)

            # Create a string so that it can be passed into ContentFile, which is readable in the FileSystem operation
            # Add 20 minutes to each home
            s = ""
            total_time_secs = 20 * 60
            for item in interpreted_route:
                total_time_secs = 20 * 60 + item[1]
                s += item[0]
                s += " "
                s += str(item[1] / 60 + 20)
                s += "\n"

            # Update Itinerary Model
            # File name is unique based on user and current time (making it impossible to have duplicates)

            itinerary_model = ItineraryModel.objects.create(client=user)
            itinerary_model.tour_duration_seconds = total_time_secs

            itinerary_model.itinerary.save(name="itinerary", content=ContentFile(s))
            for home in homes_list:
                itinerary_model.homes.add(home)

            itinerary_model.save()
            return True
        else:
            return False
