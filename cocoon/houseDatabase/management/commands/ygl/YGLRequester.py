# Django Modules
from django.utils import timezone
from django.db import IntegrityError

# Cocoon modules
from cocoon.houseDatabase.constants import YGL_URL
from cocoon.houseDatabase.models import RentDatabaseModel
from cocoon.houseDatabase.models import YglManagementModel, HomeTypeModel, HomeProviderModel
from cocoon.houseDatabase.management.commands.helpers.data_input_normalization import normalize_street_address

# Import third party libraries
import os
import sys
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from datetime import datetime
from pytz import timezone as pytimezone

# Load the logger
import logging
logger = logging.getLogger(__name__)


class YGLRequester(object):
    """
    This class contains the logic for parsing the XML
    feed from YGL and adding apartments to the database. It has been abstracted
    out of the Command class so it can be tested easily.

    Attributes:
        self.NUM_COLS (int): the number of columns in the txt file returned by MLSPIN
    """

    YGL_FEED_FILE_NAME = "ygl_feed.xml"

    def __init__(self, timestamp, ygl_file=""):
        """
        Retrieves IDX feed data from MLSPIN, including txt formatted information on
        over 4000 apartments in Massachusetts.
        """

        self.update_timestamp = timestamp
        ygl_data = ""
        if not ygl_file:
            # 1. Connect to mlspin IDX (internet data exchange URL)
            try:
                urllib.request.urlretrieve(YGL_URL, os.path.join(os.path.dirname(__file__), self.YGL_FEED_FILE_NAME))
            except (urllib.error.HTTPError, urllib.error.URLError):
                print("Error connecting to YGL")
                sys.exit()
            ygl_data = self.YGL_FEED_FILE_NAME
        else:
            ygl_data = ygl_file

        # 2. Read the response txt into memory
        self.ygl_file = ET.parse(os.path.join(os.path.dirname(__file__), ygl_data))

    def parse_idx_feed(self):
        root = self.ygl_file.getroot()

        # Reporting information
        num_houses = 0
        num_of_duplicates = 0
        num_of_value_errors = 0
        num_failed_to_update = 0
        num_integrity_error = 0
        num_updated_homes = 0
        num_added_homes = 0

        # Loop through every home
        for house in root.iter('Rental'):
            num_houses += 1
            new_listing = RentDatabaseModel()
            street_number = ""
            street_name = ""
            for element in house:
                try:
                    if element.tag == 'ID':
                        new_listing.listing_number = element.text
                    elif element.tag == 'StreetNumber':
                        street_number = element.text
                    elif element.tag == 'StreetName':
                        street_name = element.text
                    elif element.tag == 'City':
                        new_listing.city = element.text
                    elif element.tag == 'State':
                        new_listing.state = element.text
                    elif element.tag == 'Zip':
                        new_listing.zip_code = element.text
                    elif element.tag == 'UnitNumber':
                        new_listing.apartment_number = element.text.lower()
                    elif element.tag == 'Latitude':
                        new_listing.latitude = element.text
                    elif element.tag == 'Longitude':
                        new_listing.longitude = element.text
                    elif element.tag == 'Beds':
                        new_listing.num_bedrooms = int(element.text)
                    elif element.tag == 'Baths':
                        # don't support decimals right now
                        new_listing.num_bathrooms = round(float(element.text))
                    elif element.tag == 'AvailableDate':
                        date_available = datetime.strptime(element.text, '%m/%d/%Y')
                        # Need to compare non-naive timezone date to non-naive.
                        # This way the dates are comparable
                        date_available = pytimezone('US/Eastern').localize(date_available)
                        if timezone.now() > date_available:
                            new_listing.currently_available = True
                    elif element.tag == 'Parking':
                        if element.text == 'Included':
                            new_listing.parking_spot = True
                    elif element.tag == 'Price':
                        new_listing.price = int(element.text)
                    elif element.tag == 'Features':
                        new_listing.remarks = element.text

                except ValueError:
                    print("[ VALUE ERROR ] Could not add home")
                    num_of_value_errors += 1
                    continue

            new_listing.home_type = HomeTypeModel.objects.get(home_type="Apartment")
            new_listing.listing_provider = HomeProviderModel.objects.get(provider="YGL")
            new_listing.last_updated = self.update_timestamp
            new_listing.street_address = normalize_street_address("{0} {1}".format(street_number, street_name))

            # Determines if the home already exists as a YGL house
            if RentDatabaseModel.objects.filter(listing_provider=new_listing.listing_provider) \
                    .filter(listing_number=new_listing.listing_number).exists():
                existing_apartment = RentDatabaseModel.objects.get(listing_number=new_listing.listing_number)

                # If it does, then make sure the street addresses line up before updating the home
                if existing_apartment.full_address == new_listing.full_address \
                        and existing_apartment.apartment_number == new_listing.apartment_number:
                    # Since the apartments are the same, just update the values in the existing apartment
                    existing_apartment.update(new_listing)
                    existing_apartment.save()
                    print("[ UPDATED ] {0}".format(existing_apartment.full_address))
                    num_updated_homes += 1

                # If the street addresses don't line up, then mark it as an error
                else:
                    num_failed_to_update += 1
                    print("[ FAILED UPDATE ] {0}".format(existing_apartment.full_address))

            # If the home isn't an YGL house, then check to see if it could exist in another provider
            elif RentDatabaseModel.objects.filter(street_address=new_listing.street_address) \
                    .filter(apartment_number=new_listing.apartment_number):
                print("[ DUPLICATE ] " + new_listing.full_address)
                num_of_duplicates += 1
            else:
                try:
                    new_listing.save()
                    print("[ ADDING ] " + new_listing.full_address)
                    num_added_homes += 1
                except IntegrityError:
                    print("[ Integrity Error ] ")
                    num_integrity_error += 1

        manager = YglManagementModel.objects.all().first()
        manager.last_updated_ygl = self.update_timestamp
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
                    "Number of integrity error is: {0}\n".format(num_integrity_error))
