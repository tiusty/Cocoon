# noinspection PyPackageRequirements
import urllib.request
import urllib.error
from django.db import IntegrityError
import cocoon.houseDatabase.maps_requester as geolocator
import os, sys
from cocoon.houseDatabase.models import RentDatabaseModel, HomeProviderModel
from cocoon.houseDatabase.management.commands.mlspin._mls_fields import *
from config.settings.Global_Config import gmaps_api_key
from cocoon.houseDatabase.models import HomeTypeModel, HomeProviderModel
from cocoon.houseDatabase.constants import MLSpin_URL
from cocoon.houseDatabase.management.commands.helpers.data_input_normalization import normalize_street_address

# Load the logger
import logging
logger = logging.getLogger(__name__)


class MlspinRequester(object):
    """
    This class contains the logic for parsing the IDX (Internet Data Exchange)
    feed from MLSPIN and adding apartments to the database. It has been abstracted
    out of the Command class so it can be tested easily.

    Attributes:
        self.NUM_COLS (int): the number of columns in the txt file returned by MLSPIN
    """

    NUM_COLS = 29

    def __init__(self, timestamp, num_homes=-1, pull_idx_feed=True, **kwargs):
        """
        Retrieves IDX feed data from MLSPIN, including txt formatted information on
        over 4000 apartments in Massachusetts.
        """

        self.update_timestamp = timestamp

        if pull_idx_feed:
            # 1. Connect to mlspin IDX (internet data exchange URL)
            try:
                urllib.request.urlretrieve(MLSpin_URL, os.path.join(os.path.dirname(__file__), "idx_feed.txt"))
            except (urllib.error.HTTPError, urllib.error.URLError):
                print("Error connecting to MLSPIN")
                sys.exit()

            # 2. Read the response txt into memory
            with open(os.path.join(os.path.dirname(__file__), "idx_feed.txt"), "rb") as fp:
                self.idx_txt = fp.read().decode("iso-8859-1").splitlines()

            towns_file = open(os.path.join(os.path.dirname(__file__), "towns.txt"), "rb")
            towns_txt = (towns_file.read().decode("iso-8859-1"))

            self.town_txt = towns_txt

        if 'town_txt' in kwargs:
            self.town_txt = kwargs.pop('town_txt', None)

        # Builds a dictionary of town codes to towns
        self.towns = {}
        town_lines = self.town_txt.split('\n')
        # Strips any new lines. There was issues on windows due to different new lines characters
        #   This makes sure all the elements in the area do no have new line/carriage return characters
        self.town_lines = list(map(str.rstrip, town_lines))
        for line in self.town_lines[1:-1]:  # skips the col headers
            fields = line.split('|')
            self.towns[str(fields[0])] = {
                "town": fields[1],
                "county": fields[2],
                "state": fields[3]
            }

        self.num_homes = num_homes

    def parse_idx_feed(self):

        lines = self.idx_txt
        print("Attempting to add *" + str(len(lines)) + "* apartments to the db...")
        print("An equivalent number of requests will be made to the geocoder")

        # Generate values for the different error cases for tracking purposes
        num_houses = 0
        num_of_duplicates = 0
        num_of_value_errors = 0
        num_failed_to_update = 0
        num_failed_to_geolocate = 0
        num_not_for_rental = 0
        num_integrity_error = 0
        num_added_homes = 0
        num_updated_homes = 0
        num_homes_not_enough_cells = 0

        counter = 0
        for line in lines[1:]:  # skips the col headers
            # if self.num_homes is equal to -1, then it means to loop through all homes,
            #   otherwise just loop for the indicated number of homes
            if self.num_homes != -1 and counter >= self.num_homes:
                break
            counter = counter + 1
            num_houses += 1
            new_listing = RentDatabaseModel()

            # Parse IDX feed to put each item into an array
            cells = line.split('|')

            # If the home doesn't have enough cells then something is wrong with the listing and it won't
            #   be added to the database. Otherwise it will cause an exception
            if len(cells) < 28:
                print("Removing home not enough cells")
                num_homes_not_enough_cells += 1
                continue

            # Make sure there are no commas in the street name
            cells[STREET_NAME].replace(',', '')
            split_address = cells[STREET_NAME].split()

            # Needed Variables
            clean_address = ""

            try:
                # check for presence of apartment number with int()
                int(cells[STREET_NAME][len(cells[STREET_NAME])-1])
                clean_address = " ".join(split_address[:-1])
            # no int in last address element (not an apartment #)
            except ValueError:
                clean_address = " ".join(split_address)

            # If any of the fields give a value error, then don't save the apartment
            try:
                # Set the HomeBaseModel Fields
                new_listing.street_address = normalize_street_address("{0} {1}".format(cells[STREET_NO], clean_address))
                new_listing.city = self.towns[str(cells[TOWN_NUM])]["town"]
                new_listing.state = self.towns[str(cells[TOWN_NUM])]["state"]
                new_listing.zip_code = cells[ZIP_CODE]
                new_listing.price = int(cells[LIST_PRICE])

                # Set InteriorAmenitiesModel Fields
                # Currently don't support non-integers for num_bathrooms. Therefore
                #   The num of full and half baths are added then rounded to the nearest int
                num_baths = int(cells[NO_FULL_BATHS]) + int(cells[NO_HALF_BATHS])
                new_listing.bath = True if num_baths > 0 else False
                new_listing.num_bathrooms = num_baths
                new_listing.num_bedrooms = int(cells[NO_BEDROOMS])

                # Set MLSpinDataModel fields
                new_listing.remarks = cells[REMARKS]
                new_listing.listing_number = int(cells[LIST_NO])
                new_listing.listing_provider = HomeProviderModel.objects.get(provider="MLSPIN")
                new_listing.listing_agent = cells[LIST_AGENT]
                new_listing.listing_office = cells[LIST_OFFICE]
                new_listing.last_updated = self.update_timestamp

                # Set RentDatabaseModel fields
                new_listing.apartment_number = cells[UNIT_NO].lower()

                # Set Exterior Amenities fields
                if int(cells[PARKING_SPACES]) > 0:
                    new_listing.parking_spot = True

                # Create the new home
                # Define the home type
                list_type = cells[PROP_TYPE]

                # verifies unit is a rental (RN denotes rental in MLS feed)
                if list_type == "RN":
                    apartment_home_type = HomeTypeModel.objects.get(home_type="Apartment")
                else:
                    # Since we only support rentals right now we don't want to retrieve any other home types
                    print("Home not a rental, continuing. Error was with line {0}".format(line))
                    num_not_for_rental += 1
                    continue

                new_listing.home_type = apartment_home_type
                new_listing.currently_available = True

            except ValueError:
                print("Home could not be added. Error is with line: {0}".format(line))
                num_of_value_errors += 1
                continue

            if RentDatabaseModel.objects.filter(listing_provider=new_listing.listing_provider) \
                    .filter(listing_number=new_listing.listing_number):
                # If the apartment already exists on MLSpin, verify that the address is the same, if it is then continue
                #   otherwise throw an error (just for testing purposes to see if it happens). If we decide this is a
                #   non-issue, we can take this out
                existing_apartment = RentDatabaseModel.objects.get(listing_number=new_listing.listing_number)
                if existing_apartment.full_address == new_listing.full_address \
                        and existing_apartment.apartment_number == new_listing.apartment_number:

                    # The lat and long is the only thing that is not computed for each new_listing since it costs money
                    #   Therefore assume the old lat and long values are correct (Should not change)
                    new_listing.latitude = existing_apartment.latitude
                    new_listing.longitude = existing_apartment.longitude

                    # Since the apartments are the same
                    #   Update the existing apartment with the fields stored in the new listing
                    existing_apartment.update(new_listing)
                    existing_apartment.save()
                    print("[ UPDATED ] {0}".format(existing_apartment.full_address))
                    num_updated_homes += 1
                else:
                    print("[ FAILED UPDATE ] {0}".format(new_listing.full_address))
                    num_failed_to_update += 1
            elif RentDatabaseModel.objects.filter(street_address=new_listing.street_address) \
                    .filter(apartment_number=new_listing.apartment_number):
                print("[ DUPLICATE ] {0}".format(new_listing.full_address))
                num_of_duplicates += 1
            else:

                # If it is a new home then get the lat and long of the home.
                latlng = geolocator.maps_requester(gmaps_api_key).get_lat_lon_from_address(new_listing.full_address)

                if latlng == -1:
                    print("Could not generate Lat and Long for apartment {0}, which had line {1} in IDX feed".format(
                        new_listing.full_address, line
                    ))
                    num_failed_to_geolocate += 1
                    continue
                else:
                    lat = latlng[0]
                    lng = latlng[1]

                new_listing.latitude = lat
                new_listing.longitude = lng
                # After all the data is added, save the home to the database
                try:
                    new_listing.save()
                    num_added_homes += 1
                    print("[ ADDING ] " + new_listing.full_address)
                except IntegrityError:
                    print("[ Integrity Error ] ")
                    num_integrity_error += 1

        manager = HomeProviderModel.objects.get(provider="MLSPIN")
        manager.last_updated_feed = self.update_timestamp
        manager.save()

        print("")
        print("RESULTS:")
        logger.info("\nNumber of houses in database: {0}\n".format(num_houses) +
                    "Num added homes: {0}\n".format(num_added_homes) +
                    "Num updated homes: {0}\n".format(num_updated_homes) +
                    "Update timestamp: {0}\n".format(self.update_timestamp.date()) +
                    "Number of duplicates: {0}\n".format(num_of_duplicates) +
                    "Number of value errors: {0}\n".format(num_of_value_errors) +
                    "Number of failed updated houses: {0}\n".format(num_failed_to_update) +
                    "Number of failed geolocates: {0}\n".format(num_failed_to_geolocate) +
                    "Number of houses not for rental: {0}\n".format(num_not_for_rental) +
                    "Number of integrity error is: {0}\n".format(num_integrity_error) +
                    "Number of homes that don't have enough cells: {0}\n".format(num_homes_not_enough_cells))
