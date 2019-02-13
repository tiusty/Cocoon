import json
import os
from datetime import timedelta
import random
from django.utils import timezone

from ....models import ZipCodeChild, ZipCodeBase

# import googlemaps API
from click._compat import raw_input

# Retrieve Constants
from cocoon.commutes.models import CommuteType
from cocoon.commutes.distance_matrix.commute_retriever import retrieve_exact_commute

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


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

        with open(BASE_DIR + "/zip_codes_MA.txt", "r") as f:
            for line in f:
                line = line.split()
                # We are assuming that all the zipcodes are in MA
                list_zip_codes.append((str(line[0]), 'MA'))

        # Makes sures that all the zip-codes are distinct
        list_zip_codes_distinct = list(set(list_zip_codes))

        self.commute_approximations(list_zip_codes_distinct, commute_type)

    def commute_approximations(self, list_zip_codes, commute_type):
        """
        :param list_zip_codes: list of zip codes in the Boston area
        :param commute_type: (string) -> The commute type of the baseline that is being created
        :return:

        Function calls the Google Maps Distance Matrix API for every possible combination of Boston zip codes.
        The response object is then parsed for distance and duration in m, s respectively. This data is then used
        to create a dictionary, which is ultimately written to approximations.txt as a json object.
        """
        json_commute = {}
        json_commute["approximations"] = []
        commute_type_google = ""

        if commute_type == "driving":
            commute_type_google = CommuteType.objects.get_or_create(commute_type=CommuteType.DRIVING)[0]
        elif commute_type == "transit":
            commute_type_google = CommuteType.objects.get_or_create(commute_type=CommuteType.TRANSIT)[0]

        filename_out = BASE_DIR + "/baselines/zipcode_baseline_" + commute_type + ".json"

        with open(filename_out, "w") as f:
            for base_zip in list_zip_codes:

                    # map (zip, state) tuples list to a list of "state+zip" strings
                    results = retrieve_exact_commute(list(map(lambda x: x[1] + "+" + x[0], list_zip_codes)),
                                                     [base_zip[1] + "+" + base_zip[0]],
                                                     commute_type_google)
                    counter = 0
                    for commute in results:
                        json_commute["approximations"].append({
                            "origin": base_zip,
                            "destination": list_zip_codes[counter],
                            "duration": results[counter][0][0],
                            "distance": results[counter][0][1]
                        })
                        counter+=1

            f.write(json.dumps(json_commute,ensure_ascii=False))

    def update_zipcode_database(self, commute_type):
        """
        :param
        :param
        :return:

        Looks into ZipCodeBase database and creates all possible combinations and allows sends errors if approximations
        don't match baselines
        """
        filename = BASE_DIR + "/baselines/zipcode_baseline_"+commute_type+".json"

        unique_zipcodes = []

        commute_type_google = ""

        if commute_type == "driving":
            commute_type_google = CommuteType.objects.get_or_create(commute_type=CommuteType.DRIVING)[0]
        elif commute_type == "transit":
            commute_type_google = CommuteType.objects.get_or_create(commute_type=CommuteType.TRANSIT)[0]

        with open(filename, "r") as f:
            data = json.load(f)
            origin_zipcodes = []
            for item in data["approximations"]:
                origin_zipcodes.append(item.get('origin')[0])


            unique_zipcodes = list(set(origin_zipcodes))

            for item in unique_zipcodes:
                destination_zip = ZipCodeBase.objects.get(zip_code=item)

                # Retrieve all the child zip_codes for the destination commute_type
                child_zips = ZipCodeChild.objects.filter(base_zip_code=destination_zip). \
                    filter(commute_type=commute_type_google). \
                    values_list('zip_code', 'commute_time_seconds')

                # Dictionary Compression to retrieve the values from the QuerySet
                child_zip_codes = {zip_code: commute_time_seconds for zip_code, commute_time_seconds in child_zips}

                for k,v in child_zip_codes.items():
                    for zipcode_baseline in data["approximations"]:
                        origin_zipcode_baseline = zipcode_baseline.get('origin')[0]
                        destination_zipcode_baseline = zipcode_baseline.get('destination')[0]

                        if k == destination_zipcode_baseline and item == origin_zipcode_baseline:
                            if v != zipcode_baseline.get('duration'):
                                print("MISS MATCH VALUE")
                        else:
                            new_base = ZipCodeBase.objects.get(zip_code=origin_zipcode_baseline)
                            ZipCodeChild.objects.create(zip_code=destination_zipcode_baseline,
                                base_zip_code=new_base,
                                commute_time_seconds=zipcode_baseline.get('duration'),
                                commute_distance_meters=zipcode_baseline.get('distance'),
                                last_date_updated=timezone.now() - timedelta(days=random.randint(0,13)),
                                commute_type=commute_type_google
                            )


