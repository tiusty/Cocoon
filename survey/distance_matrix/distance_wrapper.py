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
    Interprets the json response dict from the googlemaps distance_matrix request.
    Handles all errors and combines distances into a list
    :param response_obj, the json response as a dictionary
    :returns a list of lists with distances between origins and their destination(s)
    """
    def interpret_distance_matrix_response(self, response_obj):
        return

    """
    Computes a distance matrix using the origins and destinations, doing multiple
    requests when origins or destinations exceed 25
    :params origins, list of origins in legal format
    :params destinations, a list of destinations in a legal format
    :returns a list of lists containing the distances between each origin and its destination(s)
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
                distance_matrix_list.append(response_list)
                origin_list = origin_list[25:]
            else:
                response_json = googlemaps.distance_matrix(self.key,
                                                           origins,
                                                           destinations,
                                                           units=self.units,
                                                           mode=self.mode)
                response_dict = json.loads(response_json)
                response_list = self.interpret_distance_matrix_response(response_dict)
                distance_matrix_list.append(response_list)
                # no origins remaining
                origin_list = []
        return distance_matrix_list