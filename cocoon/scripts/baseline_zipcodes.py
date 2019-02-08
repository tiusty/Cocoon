import json
# import googlemaps API
from googlemaps import distance_matrix, client

# import API key from settings
from config.settings.Global_Config import gmaps_api_key

class BaselineZipcodes:

    def __init__(self, key=gmaps_api_key, units="imperial"):
        self.list_zip_codes = ["02108", "02109", "02110", "02111", "02113", "02114",
                          "02115", "02116", "02118", "02119", "02120", "02121",
                          "02122", "02124", "02125", "02126", "02127", "02128",
                          "02129", "02130", "02131", "02132", "02134", "02135",
                          "02136", "02151", "02152", "02163", "02199", "02203",
                          "02210", "02215", "02467"]

        self.key = key
        self.units = units
        self.client = client.Client(self.key)

    def commute_approximations(self):

        for i in self.list_zip_codes:
            for j in self.list_zip_codes:
                response_json = distance_matrix.distance_matrix(self.client,
                                                                [i],
                                                                [j],
                                                                units=self.units)
                print(response_json)