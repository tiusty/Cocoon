# import django modules
from django.core.files.base import ContentFile

# App imports
from ..clientScheduler.base_algorithm import clientSchedulerAlgorithm
from ..models import ItineraryModel

# import distance matrix wrapper
from cocoon.commutes.distance_matrix.commute_retriever import retrieve_exact_commute_client_scheduler, retrieve_approximate_commute_client_scheduler
from cocoon.commutes.distance_matrix.commute_cache_updater import update_commutes_cache_client_scheduler

# Import Cocoon modules
from cocoon.commutes.models import CommuteType
from cocoon.commutes.constants import CommuteAccuracy


class ClientScheduler(clientSchedulerAlgorithm):

    def __init__(self, accuracy=CommuteAccuracy.EXACT):
        super().__init__()
        self.commute_accuracy = accuracy

    def build_homes_matrix(self, homes_list):
        """
        builds the homes matrix using the DistanceWrapper for now. Basically computes the distances using the Google Distance Matrix API and stores it.

        :param (list) homes_list: List of strings containing home addresses used to compute the optimal itinerary
        :return: (list): homes_matrix a nxn matrix of distances found using the DistanceWrapper() to indicate the distances betweeen any two homes
        """

        # Matrix that contains every home and the duration it takes to get to every other home in the list
        homes_matrix = []

        # Loop through every home in the list
        #   And create a list of the times between this home and the other homes
        for home in homes_list:
            home_distances = []

            # Only let them do driving
            commute_type = CommuteType.objects.get_or_create(commute_type=CommuteType.DRIVING)[0]

            # Depending on the accuracy either get the exact commute or the approximate
            if self.commute_accuracy == CommuteAccuracy.EXACT:
                result_distance_wrapper = retrieve_exact_commute_client_scheduler(homes_list, [home], commute_type)
                for commute in result_distance_wrapper:
                    time_seconds = commute[0][0]
                    distance_meters = commute[0][1]
                    if time_seconds is not None and distance_meters is not None:
                        home_distances.append(time_seconds)
            else:
                update_commutes_cache_client_scheduler(homes_list,
                                                       home,
                                                       accuracy=CommuteAccuracy.APPROXIMATE,
                                                       commute_type=CommuteType.DRIVING)
                home_distances = retrieve_approximate_commute_client_scheduler(homes_list,
                                                                               home,
                                                                               commute_type=CommuteType.DRIVING)

            homes_matrix.append(home_distances)

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
        :param homes_list: The matrix calculated using DistanceWrapper() with distances between every pair of homes in
            favourited list
        :return: (list): shortest_path List of indices that denote the shortest path, which is the output of the
            algorithms
        """

        homes_matrix = self.build_homes_matrix(homes_list)
        shortest_path = self.calculate_path(homes_matrix)
        edge_weights = self.get_edge_weights()

        tuple_list_edges = []

        for i in range(len(shortest_path)):
            temp_tuple = (shortest_path[i], edge_weights[i])
            tuple_list_edges.append(temp_tuple)

        return tuple_list_edges

    def save_itinerary(self, homes_list, user):
        """

        :param: (list) homes_list: The matrix calculated using DistanceWrapper() with distances between every pair
                                    of homes in visit list
        :param: (request.user) user: user
        :return: (boolean) -> True: The itinerary was created successfully
                              False: The itinerary was not created
        """

        if not ItineraryModel.retrieve_unfinished_itinerary(user).exists():
            total_time_secs, interpreted_route = self.calculate_duration(homes_list)
            itinerary_model = ItineraryModel(client=user)
            itinerary_model.tour_duration_seconds = total_time_secs

            # Create a string so that it can be passed into ContentFile, which is readable in the FileSystem operation
            # Add 20 minutes to each home

            # TODO: Store these values on the db

            s = b""
            for item in interpreted_route:
                line = "{0} {1}\n".format(item[0].full_address, item[1]/60 + 20).encode('utf-8')
                s += line

            itinerary_model.itinerary.save(name="itinerary", content=ContentFile(s))
            for home in homes_list:
                itinerary_model.homes.add(home)

            itinerary_model.url_slug = itinerary_model.generate_slug()
            itinerary_model.save()
            return True
        return False

    def calculate_duration(self, homes_list):
        """
        Algorithm runner
        args:
        :param: (list) homes_list: The matrix calculated using DistanceWrapper() with distances between every pair
                                    of homes in visit list
        """

        shortest_path = self.run_client_scheduler_algorithm(homes_list)
        interpreted_route = self.interpret_algorithm_output(homes_list, shortest_path)

        # Create a string so that it can be passed into ContentFile, which is readable in the FileSystem operation
        # Add 20 minutes to each home
        total_time_secs = 0
        for item in interpreted_route:
            total_time_secs = 20 * 60 + item[1] + total_time_secs

        # Update Itinerary Model
        # File name is unique based on user and current time (making it impossible to have duplicates)
        return total_time_secs, interpreted_route
