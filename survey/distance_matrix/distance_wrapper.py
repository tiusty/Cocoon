import googlemaps
from Unicorn.settings.Global_Config import gmaps_api_key
import json

"""
Class that acts as a wrapper for distance matrix requests. Splits requests into 
legal sizes and consolidates results
"""
class distance_wrapper:

    def __init__(self, key=gmaps_api_key, mode="driving", units="imperial"):
        self.key = key
        self.mode = mode
        self.units = units

    """
    handles any errors thrown by the distance_matrix API
    :param error_code, the error code returned from distance_matrix
    """
    def handle_exception(error_code):
        if (error_code == "INVALID_REQUEST"):
            raise Invalid_Request_Exception()
        elif (error_code == "MAX_ELEMENTS_EXCEEDED"):
            raise Max_Elements_Exceeded_Exception()
        elif (error_code == "OVER_QUERY_LIMIT"):
            raise Over_Query_Limit_Exception()
        elif (error_code == "REQUEST_DENIED"):
            raise Request_Denied_Exception("Check API key")
        elif (error_code == "UNKNOWN_ERROR"):
            raise Unknown_Error_Exception
        else:
            raise Exception("Unidentifiable error in distance_matrix_response")


    """
    Interprets the json response dict from the googlemaps distance_matrix request.
    Handles all errors and combines distances into a list
    :param response_obj, the json response as a dictionary
    :returns a list of lists with distances between origins and their destination(s)
    :raises Distance_Matrix_Exception
    """
    def interpret_distance_matrix_response(self, response_obj):
        # check the status
        response_status = response_obj["status"]
        if (response_status == "OK"):
            distance_list = []

            # each row is an origin
            for row in response_obj["rows"]:
                origin_distance_list = []

                # each element is the origin-destination pairing
                for element in row["elements"]:
                    element_status = element["status"]
                    if (element_status == "OK"):
                        # retrieve the duration from origin to destination
                        duration_in_minutes = int(element["duration"]["value"] / 60)
                        origin_distance_list.append(duration_in_minutes)
                    else:
                        self.handle_exception(element_status)
                distance_list.append(origin_distance_list)
        else:
            self.handle_exception(response_status)

        # list of lists of durations from origin to destinations
        return distance_list

    """
    Computes a distance matrix using the origins and destinations, doing multiple
    requests when origins or destinations exceed 25
    :params origins, list of origins in legal format
    :params destinations, a list of destinations in a legal format
    :returns a list of lists containing the distances between each origin and its destination(s)
    :raises DistanceMatrixException on invalid request
    """
    def calculate_distances(self, origins, destinations):

        distance_matrix_list = []

        if len(destinations) > 25:
            #TODO: handle exceeding destinations and merge inner response lists
            return []

        origin_list = origins
        while origin_list:
            if (len(origin_list) > 25):
                response_json = googlemaps.distance_matrix(self.key,
                                                           origins[:25],
                                                           destinations,
                                                           units=self.units,
                                                           mode=self.mode)
                response_dict = json.loads(response_json)
                response_list = self.interpret_distance_matrix_response(response_dict)
                for origin_list in response_list:
                    distance_matrix_list.append(origin_list)
                origin_list = origin_list[25:]
            else:
                response_json = googlemaps.distance_matrix(self.key,
                                                           origins,
                                                           destinations,
                                                           units=self.units,
                                                           mode=self.mode)
                response_dict = json.loads(response_json)
                response_list = self.interpret_distance_matrix_response(response_dict)
                for origin_list in response_list:
                    distance_matrix_list.append(origin_list)
                # no origins remaining
                origin_list = []

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
