import csv
import geocoder
import sys
import os
from django.core.management.base import BaseCommand, CommandError
from houseDatabase.models import HousePhotos, RentDatabase, InteriorAmenities, BuildingExteriorAmenities
from django.utils import timezone


# A command that can be executed by hooking into manage.py
# and operates on a file within this directory
#
# 'python manage.py addHouses.py <csv file name>'
# TODO: Add support for checking if addresses already exist

class Command(BaseCommand):
    help = 'Adds RentDatabase models to the database by parsing csv files\n' \
           'in the following format:\n\n' \
           'Uses: \'python manage.py addHouses <csv file in script directory>\''

    def add_arguments(self, parser):
         parser.add_argument('file', nargs='+')

    def handle(self, *args, **options):

        for str in options['file']:

            module_dir = os.path.dirname(__file__)  # get current directory
            file_path = os.path.join(module_dir, str)

            csvfile = open(file_path)
            reader = csv.reader(csvfile, delimiter=',')

            '''
            # Note: These columns may not apply to the new csv
            
            [0] Street Address
            [1] City
            [2] State
            [3] Zip Code 
            [4] Move-in Date
            [5] # Bedrooms
            [6] Home type
            [7] Rent
            [8] AC
            [9] Washer/Dryer
            [10] Dish Washer
            [11] Bath
            [12] Parking Spot
            [13] Washer/Dryer in Building
            [14] Elevator
            [15] Handicap Access
            [16] Pool / Hot Tub
            [17] Fitness Center
            [18] Storage Unit
            
            [?] # bathrooms
            '''
            for row in reader:

                # Pulls lat/lon based on address
                g = geocoder.google(row[0])
                latlng = g.latlng
                lat = latlng[0]
                lng = latlng[1]

                # TODO: Check that house doesn't exist
                # Creating a database object
                newHouse = RentDatabase
                newHouse.address = row[0]
                newHouse.city = row[1]
                newHouse.state = row[2]
                newHouse.zip_code = row[3]
                newHouse.price = int(row[4])
                newHouse.home_type = row[6]
                newHouse.move_in_day = row[4]
                newHouse.lat = lat
                newHouse.lon = lng
                newHouse.air_conditioning = True if row[8].lower() in {'yes', '1', 'true'} else False
                newHouse.wash_dryer_in_home = True if row[9].lower() in {'yes', '1', 'true'} else False
                newHouse.dish_washer = True if row[10].lower() in {'yes', '1', 'true'} else False
                newHouse.bath = True if row[11].lower() in {'yes', '1', 'true'} else False
                newHouse.num_bedrooms = int(row[5])
                newHouse.parking_spot = True if row[12].lower() in {'yes', '1', 'true'} else False
                newHouse.washer_dryer_in_building = True if row[13].lower() in {'yes', '1', 'true'} else False
                newHouse.elevator = True if row[14].lower() in {'yes', '1', 'true'} else False
                newHouse.handicap_access = True if row[15].lower() in {'yes', '1', 'true'} else False
                newHouse.pool_hot_tub = True if row[16].lower() in {'yes', '1', 'true'} else False
                newHouse.fitness_center = True if row[17].lower() in {'yes', '1', 'true'} else False
                newHouse.storage_unit = True if row[18].lower() in {'yes', '1', 'true'} else False

                newHouse.save()

                newPhotos = HousePhotos(house=newHouse)
                newPhotos.save()
                newHouse.save()

                # Num Bathrooms should be added appropriately
                newHouse.num_bathrooms = int(row[19])

                # Prints for testing purposes
                # print(row[0])
                # print("\n")

            csvfile.close()


