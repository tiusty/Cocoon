# noinspection PyPackageRequirements
import urllib.request
import urllib.error
import houseDatabase.management.commands.maps_requester as geolocator
import os, sys
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from houseDatabase.models import HousePhotosModel, RentDatabaseModel, InteriorAmenitiesModel, BuildingExteriorAmenitiesModel
from houseDatabase.management.commands.mls_fields import *
from Unicorn.settings.Global_Config import gmaps_api_key
from django.utils import timezone


class Command(BaseCommand):
    help = 'Ingests IDX feed into database'

    def add_arguments(self, parser):
        # add args here
        return

    def handle(self, *args, **options):
        URL = "http://idx.mlspin.com/idx.asp?user=2KzB9t1MntTtFUBNRt7rdWjyY2L29YztntNuRDNKn2rZhRFotmDcv7ZnDPxIt9OLf22qotUxtyT&proptype=RN"
        NUM_COLS = 29  # mlspin specific

        # 1. Connect to MLSPIN IDX (internet data exchange URL)
        try:
            urllib.request.urlretrieve(URL, os.path.join(os.path.dirname(__file__),"idx_feed.txt"))
        except (urllib.error.HTTPError,urllib.error.URLError):
            print("Error connecting to MLSPIN")
            sys.exit()

        # 2. Read the response txt into memory
        idx_file = open(os.path.join(os.path.dirname(__file__),"idx_feed.txt"), "rb")
        idx_txt = (idx_file.read().decode("iso-8859-1"))

        towns_file = open(os.path.join(os.path.dirname(__file__),"towns.txt"), "rb")
        town_txt = (towns_file.read().decode("iso-8859-1"))

        # 3. Build a dictionary of town codes to towns
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

        # 4. Parses the IDX txt
        for line in lines[2:-1]:

            #
            cells = line.split('|')
            cells[STREET_NAME].replace(',','')
            split_address = cells[STREET_NAME].split()
            apartment_no = ""
            has_apartment_no = False
            clean_address = ""

            try:
                # check for presence of apartment number with int()
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

            if (RentDatabaseModel.objects.filter(listing_no=cells[LIST_NO]).exists()):
                # this house already exists, update move in day
                existing_apartment = RentDatabaseModel.objects.get(listing_no=cells[LIST_NO])
                existing_apartment.move_in_day = datetime.now()
                existing_apartment.save()
                print("[DUPLICATE]" + full_add)
                continue
            else:
                # Pulls lat/lon based on address
                locator = geolocator.maps_requester(gmaps_api_key)
                latlng = locator.get_lat_lon_from_address(full_add)

                if (latlng == -1):
                    continue
                else:
                    lat = latlng[0]
                    lng = latlng[1]

                new_listing = RentDatabaseModel()
                new_listing.latitude_home = lat
                new_listing.longitude_home = lng
                new_listing.address = address
                new_listing.city_home = town
                new_listing.zip_code_home = zip
                new_listing.state_home = state
                new_listing.price_home = cells[LIST_PRICE]

                list_type = cells[PROP_TYPE]
                if (list_type == "RN"):
                    new_listing.home_type_survey = "Apartment"
                else:
                    print("listing not a rental")
                    continue

                new_listing.move_in_day_home = datetime.now()
                new_listing.num_bedrooms_home = int(cells[NO_BEDROOMS])
                no_baths = int(cells[NO_FULL_BATHS]) + int(cells[NO_HALF_BATHS])
                new_listing.num_bathrooms_home = no_baths
                new_listing.bath_home = True if no_baths > 0 else False
                new_listing.remarks_home = cells[REMARKS]
                new_listing.listing_no = int(cells[LIST_NO])
                new_listing.listing_provider_home = "MLSPIN"
                new_listing.listing_agent_home = cells[LIST_AGENT]
                new_listing.listing_office_home = cells[LIST_OFFICE]
                new_listing.apartment_number_home = apartment_no

                #TODO: Actually get photos based on ftp url and AWS S3
                new_listing.save()
                newPhotos = HousePhotosModel(house=new_listing)
                newPhotos.save()
                new_listing.save()
                print(full_add + " added")

        print(len(lines))