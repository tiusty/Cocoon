# Django Modules
from django.utils import timezone

# Cocoon modules
from cocoon.houseDatabase.constants import YGL_URL
from cocoon.houseDatabase.models import RentDatabaseModel
from cocoon.houseDatabase.models import YglManagementModel

# Import third party libraries
import os
import sys
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from datetime import datetime
from pytz import timezone as pytimezone


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

    def __init__(self, timestamp=timezone.now):
        """
        Retrieves IDX feed data from MLSPIN, including txt formatted information on
        over 4000 apartments in Massachusetts.
        """

        self.update_timestamp = timestamp

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

        # Reporting information
        num_of_duplicates = 0
        num_of_value_errors = 0

        # Loop through every home
        for house in root.iter('Rental'):
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

            new_listing.listing_provider = "YGL"
            new_listing.last_updated = self.update_timestamp
            new_listing.street_address = "{0} {1}".format(street_number, street_name)
            if RentDatabaseModel.objects.filter(street_address_home=new_listing.street_address)\
                    .filter(apartment_number_home=new_listing.apartment_number_home):
                print("[ DUPLICATE ]" + new_listing.full_address)
                num_of_duplicates += 1
            else:
                # new_listing.save()
                print("[ ADDING ]" + new_listing.full_address)

        manager = YglManagementModel.objects.all().first()
        manager.last_updated_ygl = self.update_timestamp
        manager.save()

        print("")
        print("RESULTS:")
        print("Update timestamp: {0}".format(self.update_timestamp.date()))
        print("Number of duplicates: {0}".format(num_of_duplicates))
        print("Number of value errors: {0}".format(num_of_value_errors))
