# import python modules
import math
from datetime import timedelta

# import django modules
from django.core.files.base import ContentFile
from django.db import transaction

# App imports
from ..clientScheduler.base_algorithm import clientSchedulerAlgorithm
from ..models import ItineraryModel, HomeVisitModel, ViableTourTimeModel

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

        :param (list) homes_list: List of RentDatabaseModel objects included in the homes matrix
        :return: (list) homes_matrix: a square matrix of travel times found using the DistanceWrapper() indicating pairwise home distances,
        where the row and column indices are preserved from the input order
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
                        home_distances.append(math.inf)
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

    def run_client_scheduler_algorithm(self, homes_list):
        """
        Creates the home matrix and calls the calculation algorithm to find the shortest path
        args:
        :param homes_list: List of RentDatabaseModel objects from which shortest path will be deduced
        :return: (list (home, time)): Ordered list of tuples containing the next home to visit on the tour and the
        driving time to that home (seconds) to that home from the previous (First entry takes 0 time)
        """

        homes_matrix = self.build_homes_matrix(homes_list)
        shortest_path = self.calculate_path(homes_matrix)
        ordered_homes = [homes_list[i] for i in shortest_path]
        edge_weights = self.get_edge_weights()

        return list(zip(ordered_homes, edge_weights))

    def generate_tour_times(self, user):
        """
        creates ViableTourTimeModel's given the client's availability, the tour order, and the driving distance
        between homes on the tour. Should be called in ItineraryClientViewset.update()
        :param (User) -> User model instance associated with client
        :return: True for success, False for failure
        """
        if ItineraryModel.retrieve_unfinished_itinerary(user).exists():
            itinerary = ItineraryModel.objects.get(client=user)
            start_times = itinerary.start_times

            for start_time in start_times.all():
                elapsed_time = 0
                for home_visit in HomeVisitModel.objects.filter(itinerary=itinerary).order_by("visit_index").all():
                    if home_visit.visit_index is not 0:
                        elapsed_time += 20 * 60
                    elapsed_time += home_visit.travel_time
                    time_slot = start_time.time + timedelta(seconds=elapsed_time)
                    _ = ViableTourTimeModel.objects.get_or_create(
                        home_visit=home_visit,
                        visit_time=time_slot)
            return True
        return False


    def save_itinerary(self, homes_list, user, survey):
        """

        :param: (list) homes_list: List of RentDatabaseModel's relevant to the itinerary. Typically sourced from an
        itinerary visit list
        :param: (request.user) user: user
        :return: (boolean) -> True: The itinerary was created successfully
                              False: The itinerary was not created
        """

        if not ItineraryModel.retrieve_unfinished_itinerary(user).exists():
            with transaction.atomic():
                total_time_secs, home_time_tours = self.calculate_duration(homes_list)
                itinerary_model = ItineraryModel(client=user)
                itinerary_model.tour_duration_seconds = total_time_secs
                itinerary_model.survey = survey
                itinerary_model.save()

                for i, (home, time) in enumerate(home_time_tours):
                    home_visit, created = HomeVisitModel.objects.get_or_create(
                        home=home,
                        itinerary=itinerary_model,
                        travel_time=time,
                        visit_index=i
                    )
                    itinerary_model.homes.add(home) # left for faster hashing
                self.home_time_tours = home_time_tours
            return True
        return False

    def calculate_duration(self, homes_list):
        """
        Algorithm runner
        args:
        :param: (list) homes_list: The list of RentDatabaseModel objects, whose pairwise distances will be calculated
        """

        home_time_tour = self.run_client_scheduler_algorithm(homes_list)

        # Add 20 minutes to each home
        total_time_secs = 0
        for home, time in home_time_tour:
            total_time_secs = 20 * 60 + time + total_time_secs

        # File name is unique based on user and current time (making it impossible to have duplicates)
        return (total_time_secs, home_time_tour)
