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
    JSON_DURATION_KEY_NAME = "duration_seconds"
    JSON_DISTANCE_KEY_NAME = "distance_meters"

    def create_baseline(self, commute_type):
        """
        :param commute_type: (string) -> The commute type that the baseline is being made for

        Function to run the command. list_zip_codes is all possible zip codes in Boston
        """
        verify = raw_input("Please don't run this script unless you are directed to, please type 'yes' to confirm: ")
        if verify.lower() != "yes":
            exit()

        # Read in all the zipcodes to compute
        list_zip_codes = set()
        with open(BASE_DIR + "/zip_codes_MA.txt", "r") as f:
            for line in f:
                line = line.split()
                # We are assuming that all the zipcodes are in MA
                list_zip_codes.add(str(line[0]))

        # Turn the set into a list
        list_zip_codes = list(list_zip_codes)

        # Retrieve all the zipcode combinations computed from google
        zipcode_combinations = self.generate_zipcode_combinations(list_zip_codes, commute_type)

        # Now write the result to the file
        filename = BASE_DIR + "/baselines/zipcode_baseline_" + commute_type.get_commute_type_display() + ".json"
        with open(filename, "w") as f:
            f.write(json.dumps(zipcode_combinations))

    @staticmethod
    def generate_zipcode_combinations(list_zip_codes, commute_type):
        """
        :param list_zip_codes: list of zip codes in the Boston area
        :param commute_type: (string) -> The commute type of the baseline that is being created
        :return:

        Function calls the Google Maps Distance Matrix API for every possible combination of Boston zip codes.
        The response object is then parsed for distance and duration in m, s respectively. This data is then used
        to create a dictionary, which is ultimately written to approximations.txt as a json object.
        """
        # Create all the combinations locally in python
        zipcode_combinations = {}
        for base_zip in list_zip_codes:

                # Retrieve the combination from Google
                results = retrieve_exact_commute(list_zip_codes,
                                                 base_zip,
                                                 mode=commute_type)

                # Store the results in python
                child_zipcodes = {}
                for commute in range(len(results)):
                    child_zipcodes[list_zip_codes[commute]] = {
                        ZipcodeBaseline.JSON_DURATION_KEY_NAME: results[commute][0][0],
                        ZipcodeBaseline.JSON_DISTANCE_KEY_NAME: results[commute][0][1]
                    }
                zipcode_combinations[base_zip] = child_zipcodes
        return zipcode_combinations

    def load_zipcode_combinations(self, commute_type):
        """
        :param
        :param
        :return:

        Looks into ZipCodeBase database and creates all possible combinations and allows sends errors if approximations
        don't match baselines
        """

        stored_zipcode_combinations = self.pull_stored_zipcode_data(commute_type)

        filename = BASE_DIR + "/baselines/zipcode_baseline_" + commute_type.get_commute_type_display() + ".json"
        with open(filename, "r") as f:
            data = json.load(f)
            for base_zipcode in data:
                for child_zipcode in data[base_zipcode]:
                    if not self.check_key(stored_zipcode_combinations, base_zipcode, child_zipcode):
                        zip_code_base = ZipCodeBase.objects.get_or_create(zip_code=base_zipcode)[0]
                        zip_code_base.zipcodechild_set.create(
                            zip_code=child_zipcode,
                            commute_distance_meters=data[base_zipcode][child_zipcode][self.JSON_DISTANCE_KEY_NAME],
                            commute_time_seconds=data[base_zipcode][child_zipcode][self.JSON_DURATION_KEY_NAME],
                        )

            print(data)

        #     for item in unique_zipcodes:
        #         destination_zip = ZipCodeBase.objects.get(zip_code=item)
        #
        #         # Retrieve all the child zip_codes for the destination commute_type
        #         child_zips = ZipCodeChild.objects.filter(base_zip_code=destination_zip). \
        #             filter(commute_type=commute_type_google). \
        #             values_list('zip_code', 'commute_time_seconds')
        #
        #         # Dictionary Compression to retrieve the values from the QuerySet
        #         child_zip_codes = {zip_code: commute_time_seconds for zip_code, commute_time_seconds in child_zips}
        #
        #         for k,v in child_zip_codes.items():
        #             for zipcode_baseline in data["approximations"]:
        #                 origin_zipcode_baseline = zipcode_baseline.get('origin')[0]
        #                 destination_zipcode_baseline = zipcode_baseline.get('destination')[0]
        #
        #                 if k == destination_zipcode_baseline and item == origin_zipcode_baseline:
        #                     if v != zipcode_baseline.get('duration'):
        #                         print("MISS MATCH VALUE")
        #                 else:
        #                     new_base = ZipCodeBase.objects.get(zip_code=origin_zipcode_baseline)
        #                     ZipCodeChild.objects.create(zip_code=destination_zipcode_baseline,
        #                         base_zip_code=new_base,
        #                         commute_time_seconds=zipcode_baseline.get('duration'),
        #                         commute_distance_meters=zipcode_baseline.get('distance'),
        #                         last_date_updated=timezone.now() - timedelta(days=random.randint(0,13)),
        #                         commute_type=commute_type_google
        #                     )

    def pull_stored_zipcode_data(self, commute_type):
        base_zipcodes = {}
        for zipcode_base in ZipCodeBase.objects.all():
            # Retrieve all the child zip_codes for the destination commute_type
            child_zips = zipcode_base.zipcodechild_set.filter(commute_type=commute_type) \
                .values_list('zip_code', 'commute_time_seconds', 'commute_distance_meters')

            # Dictionary Compression to retrieve the values from the QuerySet
            child_zip_codes = {zip_code: {
                 ZipcodeBaseline.JSON_DURATION_KEY_NAME: commute_time_seconds,
                 ZipcodeBaseline.JSON_DISTANCE_KEY_NAME: commute_distance_meters,
            }
                for zip_code, commute_time_seconds, commute_distance_meters
                in child_zips}

            base_zipcodes[zipcode_base.zip_code] = child_zip_codes
        return base_zipcodes

    @staticmethod
    def check_key(data, base_key, child_key):
        if base_key in data:
            if child_key in data[base_key]:
                return True
        return False
