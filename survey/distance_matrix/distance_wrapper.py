from googlemaps import distance_matrix, client
from Cocoon.settings.Global_Config import gmaps_api_key


class DistanceWrapper:
    """
    Class that includes the infrastructure to request the google matrix API.
    Attributes:
        self.key (String): the API key passed to the API
        self.mode (String): denotes the mode of transportation.
        i.e. "driving", "walking"
        self.units (String): denotes the unites. "imperial" or "metric"
        self.client (Client): wrapper around the API key used in the googlemaps package
    """

    def __init__(self, key=gmaps_api_key, mode="driving", units="imperial"):
        self.key = key
        self.mode = mode
        self.units = units
        self.client = client.Client(self.key)

    def handle_exception(self, error_code):
        """
        interprets a distance matrix error code and raises the correct exception
        :param error_code: a string
        :return: this function does not return
        """
        if (error_code == "INVALID_REQUEST"):
            raise Invalid_Request_Exception()
        elif (error_code == "MAX_ELEMENTS_EXCEEDED"):
            raise Max_Elements_Exceeded_Exception()
        elif (error_code == "OVER_QUERY_LIMIT"):
            raise Over_Query_Limit_Exception()
        elif (error_code == "REQUEST_DENIED"):
            raise Request_Denied_Exception()
        elif (error_code == "UNKNOWN_ERROR"):
            raise Unknown_Error_Exception
        elif (error_code == "ZERO_RESULTS"):
            raise Zero_Results_Exception

    def interpret_distance_matrix_response(self, response_obj):
        """
        interprets the response dict returned by the distance_matrix API. This function both handles errors
        and compiles the response into a list of lists of tuples.

        :param response_obj: the dictionary returned by the distance matrix API
        :return: a list of lists of tuples containing the duration and distance from each origin to each destination
        [[(int, int), (int, int)], [(int, int), (int, int)]]
        """

        # check the status
        response_status = response_obj["status"]
        if response_status == "OK":
            distance_list = []

            # each row is an origin
            for row in response_obj["rows"]:
                origin_distance_list = []

                # each element is the origin-destination pairing
                for element in row["elements"]:
                    element_status = element["status"]
                    if element_status == "OK":
                        # retrieve the duration from origin to destination
                        duration_in_seconds = int(element["duration"]["value"])
                        distance_in_meters = int(element["distance"]["value"])
                        origin_distance_list.append((duration_in_seconds, distance_in_meters))
                    # otherwise there was an error, skip this element

                if (origin_distance_list):
                    distance_list.append(origin_distance_list)
        else:
            self.handle_exception(response_status)

        # list of lists of durations from origin to destinations
        return distance_list

    def calculate_distances(self, origins, destinations):
        """
        Gets the distance matrix corresponding to a destination and an arbitrary number of origins.
        Segments requests to the distance matrix API to include a maximum of 25 origins and returns
        the consolidated results.

        :params origins: list of origins in a distance matrix accepted format
        :params destinations: the destination in a distance matrix accepted format
        :returns a list of lists of tuples containing the duration and distance between the origins and the
        destination(s). Each inner list corresponds to an origin and each of its tuples corresponds to a pairing
        between that origin and one of its destinations.
        :raises DistanceMatrixException on invalid request

        Example Input:
            origins: ["02052", "02124", "02482"]
            origins: ["2 Snow Hill Lane, Medfield MA"]
            destinations: ["Boston, MA"]
            destinations: ["23412", "159 Brattle Street, Arlington MA"]
        """

        distance_matrix_list = []

        origin_list = origins
        if (len(destinations) < 25):
            while origin_list:
                if (len(origin_list) > 25):
                    response_json = distance_matrix.distance_matrix(self.client,
                                                                    origin_list[:25/(len(destinations))],
                                                                    destinations[:24],
                                                                    units=self.units,
                                                                    mode=self.mode)
                    response_list = self.interpret_distance_matrix_response(response_json)
                    for res in response_list:
                        distance_matrix_list.append(res)
                    origin_list = origin_list[25:]

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
