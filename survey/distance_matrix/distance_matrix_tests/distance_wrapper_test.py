import unittest
from survey.distance_matrix import distance_wrapper
from survey.distance_matrix.distance_wrapper import *

'''
TODO: Hard code the requests in to avoid polling the API
TODO: Test more than 25 origins
'''

class TestDistanceWrapper(unittest.TestCase):

    def setUp(self):
        self.wrapper = distance_wrapper.DistanceWrapper()

    def test_request_denied_exception(self):
        response_obj =  {
           "destination_addresses" : [],
           "error_message" : "The provided API key is invalid.",
           "origin_addresses" : [],
           "rows" : [],
           "status" : "REQUEST_DENIED"
        }

        self.assertRaises(Request_Denied_Exception,
                          self.wrapper.interpret_distance_matrix_response, response_obj)

    def test_invalid_request_exception(self):
        response_obj =  {
           "destination_addresses" : [],
           "error_message" : "The provided API key is invalid.",
           "origin_addresses" : [],
           "rows" : [],
           "status" : "INVALID_REQUEST"
        }

        self.assertRaises(Invalid_Request_Exception,
                          self.wrapper.interpret_distance_matrix_response, response_obj)

    def test_over_query_limit_exception(self):
        response_obj =  {
           "destination_addresses" : [],
           "error_message" : "The provided API key is invalid.",
           "origin_addresses" : [],
           "rows" : [],
           "status" : "OVER_QUERY_LIMIT"
        }

        self.assertRaises(Over_Query_Limit_Exception,
                          self.wrapper.interpret_distance_matrix_response, response_obj)

    def test_zero_results_exception(self):
        response_obj =  {
           "destination_addresses" : [],
           "error_message" : "The provided API key is invalid.",
           "origin_addresses" : [],
           "rows" : [],
           "status" : "ZERO_RESULTS"
        }

        self.assertRaises(Zero_Results_Exception,
                          self.wrapper.interpret_distance_matrix_response, response_obj)

    def test_unknown_error_exception(self):
        response_obj =  {
           "destination_addresses" : [],
           "error_message" : "The provided API key is invalid.",
           "origin_addresses" : [],
           "rows" : [],
           "status" : "UNKNOWN_ERROR"
        }

        self.assertRaises(Unknown_Error_Exception,
                          self.wrapper.interpret_distance_matrix_response, response_obj)

    def test_max_elements_exceeded_exception(self):
        response_obj =  {
           "destination_addresses" : [],
           "error_message" : "",
           "origin_addresses" : [],
           "rows" : [],
           "status" : "MAX_ELEMENTS_EXCEEDED"
        }

        self.assertRaises(Max_Elements_Exceeded_Exception,
                          self.wrapper.interpret_distance_matrix_response, response_obj)

    ###############################################
    # API requests required for following functions
    ###############################################

    def test_simple(self):
        destination = ["2 Snow Hill Lane, Medfield MA"]
        origin = ["1 Dewing Path, Wellesley MA"]
        duration_list = self.wrapper.calculate_distances(destination, origin)
        self.assertEqual(len(duration_list), 1)
        self.assertEqual(len(duration_list[0]), 1)
        self.assertEqual(type(duration_list[0][0]), int)

    def test_multiple_origin(self):
        destinations = ["2 Snow Hill Lane, Medfield MA", "1 Dewing Path, Welleslsey MA"]
        origin = ["350 Prospect Street, Belmont MA"]
        duration_list = self.wrapper.calculate_distances(destinations, origin)
        self.assertEqual(len(duration_list), 2)
        for o in duration_list:
            self.assertEqual(len(duration_list[0]), 1)
            self.assertEqual(type(duration_list[0][0]), int)

    def test_multiple_destination(self):
        destinations = ["2 Snow Hill Lane, Medfield MA", "1 Dewing Path, Welleslsey MA"]
        origins = ["350 Prospect Street, Belmont MA", "159 Brattle Street, Arlington MA"]
        duration_list = self.wrapper.calculate_distances(destinations, origins)
        self.assertEqual(len(duration_list), 2)
        for o in duration_list:
            self.assertEqual(len(duration_list[0]), 2)
            self.assertEqual(type(duration_list[0][0]), int)


    '''
    The following test makes many requests to the API
    
    def test_exceeding_origins(self):
        destinations = []
        for i in range(50):
            destinations.append("2 Snow Hill Lane, Medfield MA")
        origins = ["350 Prospect Street, Belmont MA", "159 Brattle Street, Arlington MA"]
        duration_list = self.wrapper.calculate_distances(destinations, origins)
        print(duration_list)
        self.assertEqual(len(duration_list), 50)
        for o in duration_list:
            self.assertEqual(len(duration_list[0]), 2)
            self.assertEqual(type(duration_list[0][0]), int)
    '''