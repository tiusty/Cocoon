# noinspection PyPackageRequirements
from subprocess import check_output, call
import urllib.request
import urllib.error
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
    help = 'Ingests IDX feed into database'

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
        except (urllib.error.HTTPError,urllib.error.URLError):
            print("Error")
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
        count = 1
        for line in lines[:-1]:
            count += 1
            if (first_row):
                first_row = False
            else:
                cells = line.split('|')
                cells[STREET_NAME].replace(',','')
                split_address = cells[STREET_NAME].split()
                apartment_no = ""
                has_apartment_no = False
                clean_address = ""

                try:
                    int(cells[STREET_NAME][len(cells[STREET_NAME])-1])
                    apartment_no = split_address[len(split_address)-1]
                    clean_address = " ".join(split_address[:-1])
                    has_apartment_no = True
                except ValueError:
                    clean_address = " ".join(split_address)
                    has_apartment_no = False

                # combining address components
                town = (towns[str(cells[TOWN_NUM])]["town"])
                state = (towns[str(cells[TOWN_NUM])]["state"])
                address = ((cells[STREET_NO]) + ' ' + clean_address)
                zip = cells[ZIP_CODE]
                full_add = address + ' ' + town + ' ' + state + ' ' + zip

                if (RentDatabase.objects.filter(listing_no=cells[LIST_NO]).exists()):
                    # this house already exists
                    existing_apartment = RentDatabase.objects.get(listing_no=cells[LIST_NO])
                    existing_apartment.move_in_day = datetime.now()
                    existing_apartment.save()
                    print("[DUPLICATE]" + full_add)
                    continue
                else:
                    # Pulls lat/lon based on address
                    locator = geolocator.maps_requester("AIzaSyAM2vo0Iop11XHGfuaYG4u1unhl6roMckk")
                    latlng = locator.get_lat_lon_from_address(full_add)

                    if (latlng == -1):
                        continue
                    else:
                        lat = latlng[0]
                        lng = latlng[1]

                    new_listing = RentDatabase()
                    new_listing.lat = lat
                    new_listing.lon = lng
                    new_listing.address = address
                    new_listing.city = town
                    new_listing.zip_code = zip
                    new_listing.state = state
                    new_listing.price = cells[LIST_PRICE]

                    list_type = cells[PROP_TYPE]
                    if (list_type == "RN"):
                        new_listing.home_type = "Apartment"
                    else:
                        print("listing not a rental")
                        continue

                    new_listing.move_in_day = datetime.now()
                    new_listing.num_bedrooms = int(cells[NO_BEDROOMS])
                    no_baths = int(cells[NO_FULL_BATHS]) + int(cells[NO_HALF_BATHS])
                    new_listing.num_bathrooms = no_baths
                    new_listing.bath = True if no_baths > 0 else False
                    new_listing.remarks = cells[REMARKS]
                    new_listing.listing_no = int(cells[LIST_NO])
                    new_listing.listing_provider = "MLSPIN"
                    new_listing.listing_agent = cells[LIST_AGENT]
                    new_listing.listing_office = cells[LIST_OFFICE]
                    new_listing.apartment_no = apartment_no

                    #TODO: Actually get photos based on ftp url and AWS S3
                    new_listing.save()
                    newPhotos = HousePhotos(house=new_listing)
                    newPhotos.save()
                    new_listing.save()
                    print(full_add + " added")

        print(len(lines))