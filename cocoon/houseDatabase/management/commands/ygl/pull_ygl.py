# Django Modules
from django.utils import timezone

# Cocoon modules
from cocoon.houseDatabase.constants import YGL_URL
from cocoon.houseDatabase.models import RentDatabaseModel

# Import third party libraries
import os
import sys
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET


class YGLRequester(object):
    """
    This class contains the logic for parsing the XML
    feed from YGL and adding apartments to the database. It has been abstracted
    out of the Command class so it can be tested easily.

    Attributes:
        self.NUM_COLS (int): the number of columns in the txt file returned by MLSPIN
    """

    NUM_COLS = 29
    YGL_FEED_FILE_NAME = "ygl_feed.xml"

    def __init__(self):
        """
        Retrieves IDX feed data from MLSPIN, including txt formatted information on
        over 4000 apartments in Massachusetts.
        """

        # 1. Connect to mlspin IDX (internet data exchange URL)
        try:
            urllib.request.urlretrieve(YGL_URL, os.path.join(os.path.dirname(__file__), self.YGL_FEED_FILE_NAME))
        except (urllib.error.HTTPError, urllib.error.URLError):
            print("Error connecting to YGL")
            sys.exit()

        # 2. Read the response txt into memory
        self.ygl_file = ET.parse(os.path.join(os.path.dirname(__file__), self.YGL_FEED_FILE_NAME))

    def parse_idx_feed(self):
        root = self.ygl_file.getroot()

        # The date for all the homes that they were updated on.
        #   They use all the same times in case the day go past midnight while updating
        update_timestamp = timezone.now()

        # Loop through every home
        for house in root.iter('Rental'):
            new_listing = RentDatabaseModel()
            street_number = ""
            street_name = ""
            for element in house:
                try:
                    new_listing.listing_provider = "YGL"

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
                        new_listing.apartment_number = int(element.text)
                    elif element.tag == 'Latitude':
                        new_listing.latitude = element.text
                    elif element.tag == 'Longitude':
                        new_listing.longitude = element.text
                    elif element.tag == 'Beds':
                        new_listing.num_bedrooms = int(element.text)
                    elif element.tag == 'Baths':
                        new_listing.num_bathrooms = int(element.text)
                    elif element.tag == 'AvailableDate':
                        # Make sure to change this depending on when the available date is
                        new_listing.currently_available = True
                    elif element.tag == 'Price':
                        new_listing.price = int(element.text)

                    new_listing.last_updated = update_timestamp
                    new_listing.street_address = "{0} {1}".format(street_number, street_name)
                    new_listing.save()

                    print("[ ADDING   ]" + new_listing.full_address)

                except ValueError:
                    print("value error occurred")
