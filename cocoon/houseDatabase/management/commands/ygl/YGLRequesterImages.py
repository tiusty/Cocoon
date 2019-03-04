# Core Django Imports
from django.core.files.images import ImageFile

# Import from houseDatabase app
from cocoon.houseDatabase.models import RentDatabaseModel, HousePhotos, HomeProviderModel

# Third party imports
import xml.etree.ElementTree as ET
import os
import urllib.request
import urllib.error

# Load the logger
import logging
logger = logging.getLogger(__name__)


class YGLRequesterImage(object):
    """
    This class implements the logic to retrieve all the images for homes on the server
    The homes must already be saved onto the Cocoon database. This will iterate through all the elements
    in the xml file and add images to any home that matches the xml file

    Attributes:
        self.YGL_FEED_FILE_NAME (string) -> The default file name to load the ygl data feed
        self.update_timestamp (django.utils.timezone) -> The time that the homes were last updated
        self.ygl_file (xml file parser) -> The xml file loaded into memory that the class is going to use
    """

    YGL_FEED_FILE_NAME = "ygl_feed.xml"

    def __init__(self, timestamp, ygl_file=""):
        self.update_timestamp = timestamp
        self.num_url_errors = 0
        self.num_HTTP_errors = 0
        self.num_value_errors = 0

        if not ygl_file:
            ygl_data = self.YGL_FEED_FILE_NAME
        else:
            ygl_data = ygl_file

        # 2. Read the response txt into memory
        self.ygl_file = ET.parse(os.path.join(os.path.dirname(__file__), ygl_data))

    def run(self):
        self.add_images()
        self.print_results()

    def add_images(self):
        root = self.ygl_file.getroot()

        # Loops through all the homes in the current xml file downloaded from the home request
        for houses in root.iter('Rental'):
            house = ""
            id_found = False
            counter = 0

            # Checks to see if the ID of the home in the xml file matches any home in the database that is for YGL
            for element in houses:
                if element.tag == 'ID':
                    # If there is a match then mark a match and store the house
                    if RentDatabaseModel.objects.filter(last_updated=self.update_timestamp)\
                            .filter(listing_provider=HomeProviderModel.objects.get(provider="YGL"))\
                            .filter(listing_number=element.text).exists():
                        house = RentDatabaseModel.objects.filter(last_updated=self.update_timestamp)\
                            .filter(listing_provider=HomeProviderModel.objects.get(provider="YGL"))\
                            .get(listing_number=element.text)
                        id_found = True

                # If a home was found then add the photos to the home
                if id_found and element.tag == 'Photos':
                    if not house.images.exists():
                        for photo in element:
                            # Stores the image in a tempfile
                            try:
                                file = urllib.request.urlretrieve(photo.text)
                                file_name = "{0}_{1}.jpg".format(house.id, counter)
                                with open(file[0], "rb+") as f:
                                    new_photos = HousePhotos(house=house)
                                    new_photos.image.save(os.path.basename(file_name), ImageFile(f))
                                    counter += 1
                                urllib.request.urlcleanup()
                            except urllib.error.HTTPError:
                                self.num_HTTP_errors += 1
                                print('HTTPError occurred')
                                continue
                            except urllib.error.URLError:
                                self.num_url_errors += 1
                                print('URLError occurred')
                                continue
                            except ValueError:
                                self.num_value_errors += 1
                                print('value error')
                                continue

                        print("[ ADDED PHOTOS ] " + house.full_address)
                    else:
                        print("[ ALL SET ] " + house.full_address)

    def print_results(self):
        logger.info("\n YGL Images done uploading.\n" +
                    "Number of HTTP Errors {0}\n".format(self.num_HTTP_errors) +
                    "Number of URL Errors: {0}\n".format(self.num_url_errors) +
                    "Number of Value Errors: {0}\n".format(self.num_value_errors))
