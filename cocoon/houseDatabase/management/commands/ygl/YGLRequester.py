# Django Modules
from django.utils import timezone
from django.db import IntegrityError

# Cocoon modules
from cocoon.houseDatabase.constants import YGL_URL, CURRENTLY_AVAILABLE_DELTA_DAYS
from cocoon.houseDatabase.models import RentDatabaseModel
from cocoon.houseDatabase.models import HomeProviderModel, HomeTypeModel
from cocoon.houseDatabase.management.commands.helpers.data_input_normalization import normalize_street_address
from cocoon.houseDatabase.management.commands.helpers.word_scraper import WordScraper

# Import third party libraries
import os
import sys
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
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
                        new_listing.date_available = date_available
                        # Need to compare non-naive timezone date to non-naive.
                        # This way the dates are comparable
                        date_available = pytimezone('US/Eastern').localize(date_available)
                        if timezone.now() > date_available - timedelta(days=CURRENTLY_AVAILABLE_DELTA_DAYS):
                            new_listing.currently_available = True
                        else:
                            new_listing.currently_available = False
                    elif element.tag == 'Pet':
                        if 'Dog Ok' in element.text:
                            new_listing.dogs_allowed = True
                        elif 'Cat Ok' in element.text:
                            new_listing.cats_allowed = True
                        elif 'Pet Friendly' in element.text:
                            new_listing.dogs_allowed = True
                            new_listing.cats_allowed = True
                        elif 'Negotiable' in element.text:
                            new_listing.dogs_allowed = True
                            new_listing.cats_allowed = True
                    elif element.tag == 'Parking':
                        if element.text == 'Included':
                            new_listing.parking_spot = True
                    elif element.tag == 'Price':
                        new_listing.price = int(element.text)
                    elif element.tag == 'Features':
                        # Initialize word scraper
                        word_scraper = WordScraper(element.text)

                        if word_scraper.word_finder(["laundromat"]):
                            new_listing.laundromat_nearby = True

                        new_listing.furnished = word_scraper.word_finder(["furnished"])
                        new_listing.hardwood_floors = word_scraper.look_for_hardwood_floors()
                        new_listing.dishwasher = word_scraper.word_finder(["dishwasher"]) \
                            or word_scraper.word_finder(['dish', 'washer'])

                        if (word_scraper.word_finder(["air", "conditioning"])) \
                                or word_scraper.word_finder(["ac"])\
                                or word_scraper.word_finder(["a", "/", "c"]):
                            new_listing.air_conditioning = True

                        if word_scraper.word_finder(["pool"]) or word_scraper.word_finder(["hot", "tub"]):
                            new_listing.pool = True
                        if word_scraper.word_finder(["balcony"]) or word_scraper.word_finder(["patio"]):
                            new_listing.patio_balcony = True

                        new_listing.laundry_in_building = word_scraper.look_for_laundry_in_building()
                        new_listing.laundry_in_unit = word_scraper.look_for_laundry_in_unit()

                        new_listing.gym = word_scraper.word_finder(["gym"]) or word_scraper.word_finder(
                            ["fitness", "center"])
                        new_listing.storage = word_scraper.word_finder(["storage"])
                        new_listing.remarks = element.text

                except ValueError:
                    print("[ VALUE ERROR ] Could not add home")
                    num_of_value_errors += 1
                    continue

            new_listing.home_type = HomeTypeModel.objects.get(home_type=HomeTypeModel.APARTMENT)
            new_listing.listing_provider = HomeProviderModel.objects.get(provider="YGL")
            new_listing.last_updated = self.update_timestamp
            new_listing.street_address = normalize_street_address("{0} {1}".format(street_number, street_name))

            # Determines if the home already exists as a YGL house
            if RentDatabaseModel.objects\
                    .filter(listing_provider=new_listing.listing_provider) \
                    .filter(street_address=new_listing.street_address)\
                    .filter(city=new_listing.city) \
                    .filter(state=new_listing.state)\
                    .filter(zip_code=new_listing.zip_code)\
                    .filter(apartment_number=new_listing.apartment_number)\
                    .exists():

                # Retrieve the home that the home matches
                existing_apartment = RentDatabaseModel.objects.get(
                    street_address=new_listing.street_address,
                    city=new_listing.city,
                    state=new_listing.state,
                    zip_code=new_listing.zip_code,
                    apartment_number=new_listing.apartment_number
                )

                existing_apartment.update(new_listing)
                existing_apartment.save()
                num_updated_homes += 1
                print("[ UPDATED ] {0}".format(existing_apartment.full_address))

            # Tests if the home exists within another provider
            #   If so mark it as a duplicate and don't add it
            elif RentDatabaseModel.objects\
                    .filter(street_address=new_listing.street_address) \
                    .filter(city=new_listing.city) \
                    .filter(state=new_listing.state) \
                    .filter(zip_code=new_listing.zip_code)\
                    .filter(apartment_number=new_listing.apartment_number)\
                    .exists():
                num_of_duplicates += 1
                print("[ DUPLICATE ] " + new_listing.full_address)
            else:
                try:
                    new_listing.save()
                    print("[ ADDING ] " + new_listing.full_address)
                    num_added_homes += 1
                except IntegrityError:
                    print("[ Integrity Error ] ")
                    num_integrity_error += 1

        manager = HomeProviderModel.objects.get(provider="YGL")
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
                    "Number of integrity error is: {0}\n".format(num_integrity_error))
