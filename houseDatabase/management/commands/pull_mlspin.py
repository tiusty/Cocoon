from subprocess import check_output, call
import urllib.request
import houseDatabase.management.commands.maps_requester as geolocator
import shutil
import re
import geocoder
import sys
import os
import string
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from houseDatabase.models import HousePhotos, RentDatabase, InteriorAmenities, BuildingExteriorAmenities
from django.utils import timezone


class Command(BaseCommand):
    help: '''Parses the mlspin idx feed, validates rentals and 
	incorporates them into the database
	'''

    def add_arguments(self, parser):
        # add args here
        return

    def handle(self, *args, **options):
        URL = "http://idx.mlspin.com/idx.asp?user=2KzB9t1MntTtFUBNRt7rdWjyY2L29YztntNuRDNKn2rZhRFotmDcv7ZnDPxIt9OLf22qotUxtyT&proptype=RN"


        NUM_COLS = 29  # mlspin specific

        # ==================================#
        # For saving the IDX feed to a file
        # ==================================#

        try:
            urllib.request.urlretrieve(URL, os.path.join(os.path.dirname(__file__),"idx_feed.txt"))
        except (urllib.error):
            print(e)
            call(["curl", "-s", URL, "-o", "idx_feed.txt"])

        idx_file = open(os.path.join(os.path.dirname(__file__),"idx_feed.txt"), "rb")
        idx_txt = (idx_file.read().decode("iso-8859-1"))

        towns_file = open(os.path.join(os.path.dirname(__file__),"towns.txt"), "rb")
        town_txt = (towns_file.read().decode("iso-8859-1"))

        # mapping of town_no to town
        towns = {}

        town_lines = town_txt.split('\r\n')
        first_line = True
        for line in town_lines[:-1]:
            if (first_line):
                first_line = False
            else:
                fields = line.split('|')
                towns[str(fields[0])] = {
                    "town":fields[1],
                    "county":fields[2],
                    "state":fields[3]
                }
        lines = idx_txt.split('\r\n')

        # ==================================#
        # For reading the IDX feed to memory
        # ==================================#

        # idx_response = urllib.request.urlopen(URL)
        # idx_byte_data = idx_response.read()
        # idx_text = str(idx_byte_data)

        # splits on '|' or carriage return

        # data_cells = re.split(r'\||\n', idx_txt)

        PROP_TYPE = 0
        LIST_NO = 1
        LIST_AGENT = 2
        LIST_OFFICE = 3
        STATUS = 4
        LIST_PRICE = 5
        STREET_NO = 6
        STREET_NAME = 7
        UNIT_NO = 8
        TOWN_NUM = 9
        AREA = 10
        ZIP_CODE = 11
        LENDER_OWNED = 12
        REMARKS = 13
        PHOTO_COUNT = 14
        PHOTO_DATE = 15
        PHOTO_MASK = 16
        COUNTY = 17
        STATE = 18
        RN_TYPE = 19
        NO_ROOMS = 20
        NO_BEDROOMS = 21
        NO_FULL_BATHS = 22
        NO_HALF_BATHS = 23
        MASTER_BATH = 24
        PARKING_SPACES = 25
        LOT_SIZE = 26
        SQUARE_FEET = 27
        NO_BATHS = 28

        first_row = True
        for line in lines[:-1]:
            if (first_row):
                first_row = False
            else:
                cells = line.split('|')
                found_location = True

                cells[STREET_NAME].replace(',','')
                split_address = cells[STREET_NAME].split()

                clean_address = " ".join(split_address[:-1])

                town = (towns[str(cells[TOWN_NUM])]["town"])
                state = (towns[str(cells[TOWN_NUM])]["state"])
                address = ((cells[STREET_NO]) + ' ' + clean_address)
                zip = cells[ZIP_CODE]
                full_add = address + ' ' + town + ' ' + state + ' ' + zip

                # Pulls lat/lon based on address
                locator = geolocator.maps_requester("AIzaSyBuecmo6t0vxQDhC7dn_XbYqOu0ieNmO74")

                latlng = locator.get_lat_lon_from_address(full_add)
                print(latlng)
