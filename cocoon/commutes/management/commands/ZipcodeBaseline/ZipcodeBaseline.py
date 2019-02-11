import json
import os

# import googlemaps API
from click._compat import raw_input
from googlemaps import distance_matrix, client

# import API key from settings
from config.settings.Global_Config import gmaps_api_key

# Retrieve Constants
from cocoon.commutes.constants import GoogleCommuteNaming

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ZipcodeBaseline(object):

    def create_baseline(self, commute_type):
        """
        :param commute_type: (string) -> The commute type that the baseline is being made for

        Function to run the command. list_zip_codes is all possible zip codes in Boston
        """
        verify = raw_input("Please don't run this script unless you are directed to, please type 'yes' to confirm: ")
        if verify.lower() != "yes":
            exit()

        list_zip_codes = []

        with open(BASE_DIR + "/ZipcodeBaseline/zip_codes_MA.txt", "r") as f:
            for line in f:
                line = line.split()
                list_zip_codes.append(str(line[0]))

        # Makes sures that all the zip-codes are distinct
        list_zip_codes_distinct = list(set(list_zip_codes))

        client_google = client.Client(gmaps_api_key)

        self.commute_approximations(client_google, list_zip_codes_distinct, commute_type)

    def commute_approximations(self, client, list_zip_codes, commute_type):
        """
        :param client: google maps client
        :param list_zip_codes: list of zip codes in the Boston area
        :return:

        Function calls the Google Maps Distance Matrix API for every possible combination of Boston zip codes.
        The response object is then parsed for distance and duration in m, s respectively. This data is then used
        to create a dictionary, which is ultimately written to approximations.txt as a json object.
        """
        json_commute = {}
        json_commute["approximations"] = []
        commute_type_google = ""

        if commute_type == "driving":
            commute_type_google = GoogleCommuteNaming.DRIVING
        elif commute_type == "transit":
            commute_type_google = GoogleCommuteNaming.TRANSIT

        filename_out = BASE_DIR + "/commands/baselines/zipcode_baseline_" + commute_type + ".txt"

        with open(filename_out, "w") as f:
            for i in list_zip_codes:
                for j in list_zip_codes:
                    response_json = distance_matrix.distance_matrix(client,
                                                                [i],
                                                                [j],
                                                                mode=commute_type_google,
                                                                units="imperial")

                    json_commute["approximations"].append({
                        "origin":i,
                        "desination":j,
                        "duration":response_json.get("rows")[0].get("elements")[0].get("duration").get("value"),
                        "distance":response_json.get("rows")[0].get("elements")[0].get("distance").get("value")
                    })

            f.write(json.dumps(json_commute,ensure_ascii=False))
