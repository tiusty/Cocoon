# import googlemaps API
from googlemaps import distance_matrix, client

# import API key from settings
from config.settings.Global_Config import gmaps_api_key

# Retrieve Constants
from cocoon.commutes.constants import TRAFFIC_MODEL_BEST_GUESS, TRAFFIC_MODEL_PESSIMISTIC, GoogleCommuteNaming

# App Modules
from ..compute_departure_time import compute_departure_time_with_traffic, compute_departure_time_without_traffic

# Load the logger
import logging
logger = logging.getLogger(__name__)


class DistanceWrapper:
    """
    Class that includes the infrastructure to request the google matrix API.
    Attributes:
        self.key (String): the API key passed to the API
        i.e. "driving", "walking"
        self.units (String): denotes the unites. "imperial" or "metric"
        self.client (Client): wrapper around the API key used in the googlemaps package
    """

    def __init__(self, key=gmaps_api_key, units="imperial"):
        self.key = key
        self.units = units
        self.client = client.Client(self.key)

    @staticmethod
    def handle_exception(error_code):
        """
        interprets a distance matrix error code and raises the correct exception
        :param error_code: a string
        :return: this function does not return
        """
        if error_code == "INVALID_REQUEST":
            logger.warning("INVALID_REQUEST")
            raise Invalid_Request_Exception()
        elif error_code == "MAX_ELEMENTS_EXCEEDED":
            logger.warning("MAX_ELEMENTS_EXCEEDED")
            raise Max_Elements_Exceeded_Exception()
        elif error_code == "OVER_QUERY_LIMIT":
            logger.warning("OVER_QUERY_LIMIT")
            raise Over_Query_Limit_Exception()
        elif error_code == "REQUEST_DENIED":
            logger.error("REQUEST_DENIED")
            raise Request_Denied_Exception()
        elif error_code == "UNKNOWN_ERROR":
            logger.warning("UNKNOWN_ERROR")
            raise Unknown_Error_Exception
        elif error_code == "ZERO_RESULTS":
            logger.warning("ZERO_RESULTS")
            raise Zero_Results_Exception

    def interpret_distance_matrix_response(self, response_obj, mode, with_traffic):
        """
        interprets the response dict returned by the distance_matrix API. This function both handles errors
        and compiles the response into a list of lists of tuples.

        :param with_traffic: (Boolean) -> Determines whether or not the user specified with traffic
        :param mode: (GoogleCommuteNaming) -> The commute type the user wants
        :param response_obj: the dictionary returned by the distance matrix API
        :return: a list of lists of tuples containing the duration and distance from each origin to each destination
        [[(int, int), (int, int)], [(int, int), (int, int)]]
        """

        # check the status
        response_status = response_obj["status"]
        distance_list = []
        if response_status == "OK":

            # each row is an origin
            for row in response_obj["rows"]:
                origin_distance_list = []

                # each element is the origin-destination pairing
                for element in row["elements"]:
                    element_status = element["status"]
                    if element_status == "OK":
                        # retrieve the duration from origin to destination

                        # If the user specified driving with traffic then return the traffic time
                        if with_traffic and mode == GoogleCommuteNaming.DRIVING:
                            # Sometimes the duration in traffic doesn't exist so if it doesn't,
                            #   then take the normal durations
                            if 'duration_in_traffic' in element:
                                duration_in_seconds = int(element["duration_in_traffic"]["value"])
                            else:
                                logger.error("Duration in seconds doesn't exist: {0}".format(response_obj))
                                duration_in_seconds = int(element["duration"]["value"])
                        # Otherwise return the default duration
                        else:
                            duration_in_seconds = int(element["duration"]["value"])
                        distance_in_meters = int(element["distance"]["value"])
                        origin_distance_list.append((duration_in_seconds, distance_in_meters))
                    # otherwise there was an error, skip this element

                if origin_distance_list:
                    distance_list.append(origin_distance_list)
                else:
                    distance_list.append([(None, None)])
        else:
            self.handle_exception(response_status)

        # list of lists of durations from origin to destinations
        return distance_list

    @staticmethod
    def determine_departure_time(mode, with_traffic):
        """
        Determines the departure time depending on the commute type and whether or not they want traffic
        :param mode: (GoogleCommuteNaming) -> The commute type the user wants
        :param with_traffic: (Boolean) -> Determines whether or not the user wants traffic to be included
        :return: (int) -> The departure time in unix seconds
        """

        # Determines if the departure time should be with traffic or not
        during_traffic = False

        # Since the transit value is only accurate during rush hour, then use the rush hour time
        if mode == GoogleCommuteNaming.TRANSIT:
            during_traffic = True
        # If the user wants traffic with driving then use the rush hour departure time
        elif with_traffic and mode == GoogleCommuteNaming.DRIVING:
            during_traffic = True
        # If the user does not want traffic with driving then use a non-rush hour time
        elif not with_traffic and mode == GoogleCommuteNaming.DRIVING:
            during_traffic = False

        # Depending on what the user wants get the timestamp corresponding to the desired time
        if during_traffic:
            return compute_departure_time_with_traffic()
        else:
            return compute_departure_time_without_traffic()

    @staticmethod
    def determine_traffic_model(mode, with_traffic):
        """
        Determines the traffic model to use based on the commute type and if the user wants traffic
        :param mode: (GoogleCommuteNaming) -> The commute type the user wants
        :param with_traffic: (Boolean) -> Determines whether or not the user wants traffic to be included
        :return: (string) -> Which traffic model to use
        """
        if mode == GoogleCommuteNaming.TRANSIT:
            traffic_model = TRAFFIC_MODEL_BEST_GUESS
        elif with_traffic and GoogleCommuteNaming.DRIVING:
            traffic_model = TRAFFIC_MODEL_PESSIMISTIC
        elif not with_traffic and GoogleCommuteNaming.DRIVING:
            traffic_model = TRAFFIC_MODEL_BEST_GUESS
        else:
            traffic_model = TRAFFIC_MODEL_BEST_GUESS

        return traffic_model

    def get_durations_and_distances(self, origins, destinations_input, mode=GoogleCommuteNaming.DRIVING, with_traffic=False):
        """
        NOTE: THIS SHOULD NOT BE CALLED DIRECTLY

        To update the cache please use the commute_cache_updater
        To retrieve an exact commute please use the commute_retriever function

        Gets the distance matrix corresponding to a destination and an arbitrary number of origins.
        Segments requests to the distance matrix API to include a maximum of 25 origins and returns
        the consolidated results.

        :param origins: (list(HomeCommute)) -> List of origins as a HomeCommute
        :param destinations_input: (HomeCommute or list(HomeCommute) -> The destination or destinations for the commute
        :param mode: (GoogleCommuteNaming) -> Must be the mode using the google distance defined mode i.e from the
            GoogleCommuteNaming class
        :returns a list of lists of tuples containing the duration and distance between the origins and the
        destination(s). Each inner list corresponds to an origin and each of its tuples corresponds to a pairing
        between that origin and one of its destinations.
        :raises DistanceMatrixException on invalid request

        Example Output:
        ('12323', '232323')
        (duration_in_seconds, distance_in_meters)
        """

        distance_matrix_list = []
        origin_list = origins

        # Make sure the destinations is a list
        if isinstance(destinations_input, (list,)):
            destinations = destinations_input
        else:
            destinations = [destinations_input]

        # maximizes 100 elements while retaining 25 origin/dest limit
        destination_number = int(min(25, len(destinations)))
        origin_number = int(min((100 / destination_number), 25))

        # traffic option set to best_guess (default)
        traffic_model = self.determine_traffic_model(mode, with_traffic)

        # Determines the departure time to give more accurate commute information
        departure_time = self.determine_departure_time(mode, with_traffic)

        while origin_list:
            # only computes for the first destination_number destinations

            response_json = distance_matrix.distance_matrix(self.client,
                                                            [i.return_commute() for i in origin_list[:origin_number]],
                                                            [i.return_commute() for i in destinations[:destination_number]],
                                                            units=self.units,
                                                            mode=mode,
                                                            departure_time=departure_time,
                                                            traffic_model=traffic_model,
                                                            )

            response_list = self.interpret_distance_matrix_response(response_json, mode, with_traffic)
            # each inner list the entire results of an origin
            for res in response_list:
                distance_matrix_list.append(res)
            origin_list = origin_list[origin_number:]

        # consolidated list containing an inner list for each origin with the duration
        # in minutes to all of its destinations
        return distance_matrix_list


class Distance_Matrix_Exception(Exception):
    pass


class Invalid_Request_Exception(Distance_Matrix_Exception):
    pass


class Max_Elements_Exceeded_Exception(Distance_Matrix_Exception):
    pass


class Over_Query_Limit_Exception(Distance_Matrix_Exception):
    pass


class Request_Denied_Exception(Distance_Matrix_Exception):
    pass


class Unknown_Error_Exception(Distance_Matrix_Exception):
    pass


class Not_Found_Exception(Distance_Matrix_Exception):
    pass


class Zero_Results_Exception(Distance_Matrix_Exception):
    pass


class Max_Route_Length_Exception(Distance_Matrix_Exception):
    pass
