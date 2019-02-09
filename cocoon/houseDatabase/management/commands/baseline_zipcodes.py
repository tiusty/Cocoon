import json

# import googlemaps API
from googlemaps import distance_matrix, client

# import API key from settings
from config.settings.Global_Config import gmaps_api_key

from django.core.management.base import BaseCommand

class Command(BaseCommand):

    def handle(self, *args, **options):
        """
        :param args:
        :param options:
        :return:

        Function to run the command. list_zip_codes is all possible zip codes in Boston. The handler
        calls the commute_approximation function, which writes the JSON file "approximations.txt"
        """

        list_zip_codes = ["02108", "02109", "02110", "02111", "02113", "02114",
                               "02115", "02116", "02118", "02119", "02120", "02121",
                               "02122", "02124", "02125", "02126", "02127", "02128",
                               "02129", "02130", "02131", "02132", "02134", "02135",
                               "02136", "02151", "02152", "02163", "02199", "02203",
                               "02210", "02215", "02467"]


        units = "imerial"
        client_google = client.Client(gmaps_api_key)

        self.commute_approximations(units, client_google, list_zip_codes)


    def commute_approximations(self, units, client, list_zip_codes):
        """
        :param units: "imerial"
        :param client: google maps client
        :param list_zip_codes: list of zip codes in the Boston area
        :return:

        Function calls the Google Maps Distance Matrix API for every possible combination of Boston zip codes.
        The response object is then parsed for distance and duration in m, s respectively. This data is then used
        to create a dictionary, which is ultimately written to approximations.txt as a json object.
        """
        json_commute = {}
        json_commute["approximations"] = []
        with open("approximations.txt", "w") as f:
            for i in list_zip_codes:
                for j in list_zip_codes:
                    response_json = distance_matrix.distance_matrix(client,
                                                                [i],
                                                                [j],
                                                                units=units)

                    json_commute["approximations"].append({
                        "origin":i,
                        "desination":j,
                        "duration":response_json.get("rows")[0].get("elements")[0].get("duration").get("value"),
                        "distance":response_json.get("rows")[0].get("elements")[0].get("distance").get("value")
                    })


            f.write(json.dumps(json_commute,ensure_ascii=False))
