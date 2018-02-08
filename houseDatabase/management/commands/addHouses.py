import csv
import geocoder
import sys
import os
import string
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from houseDatabase.models import HousePhotosModel, RentDatabaseModel, InteriorAmenitiesModel, BuildingExteriorAmenitiesModel
from django.utils import timezone

'''

This script is used to automate integration of manually
generated apartment data, complying with the column
labels defined below. 

Note: Error checking has not been implemented so 
data must fit the correct format

'''

# A command that can be executed by hooking into manage.py
# and operates on a file within this directory
#
# 'python manage.py addHouses.py <csv file name>'
# TODO: Add support for checking if addresses already exist

class Command(BaseCommand):
    help = 'Adds RentDatabaseModel models to the database by parsing csv files\n' \
           'in the following format:\n\n' \
           'Uses: \'python manage.py addHouses <csv file in script directory>\''

    def add_arguments(self, parser):
         parser.add_argument('file', nargs='+')

    def handle(self, *args, **options):

        for the_str in options['file']:

            module_dir = os.path.dirname(__file__)  # get current directory
            file_path = os.path.join(module_dir, the_str)

            csvfile = open(file_path)
            reader = csv.reader(csvfile, delimiter=',')

            '''
            # Note: These columns may not apply to the new csv
            
            [0] Street Address
            [1] City
            [2] ZIp Code
            [3] State 
            [4] Move-in Date
            [5] # Bedrooms
            [6] # Bathrooms
            [7] Home type
            [8] Rent
            [9] AC
            [10] Washer/Dryer
            [11] Dish Washer
            [12] Bath
            [13] Parking Spot
            [14] Washer/Dryer in Building
            [15] Elevator
            [16] Handicap Access
            [17] Pool / Hot Tub
            [18] Fitness Center
            [19] Storage Unit
            
            '''
            firstRow = True

            for row in reader:

                if (firstRow):
                    firstRow = False
                else:

                    foundLocation = True

                    # Pulls lat/lon based on address
                    try:
                        g = geocoder.google(row[0])
                        latlng = g.latlng
                        lat = latlng[0]
                        lng = latlng[1]

                    except ValueError:
                        foundLocation = False
                        print('Could not locate: ' + row[0])

                    # TODO: Check that house doesn't exist
                    # Creating a database object

                    print(row[2])

                    if (foundLocation):

                        newHouse = RentDatabaseModel()
                        newHouse.address = row[0]
                        newHouse.city = row[1]
                        newHouse.zip_code = row[2]
                        newHouse.state = row[3]
                        newHouse.price = row[8]
                        newHouse.home_type = row[7]

                        move_in = row[4]
                        move_in_date = datetime.strptime(move_in, "%m/%d/%Y")
                        fixed_date = datetime.strftime(move_in_date, "%Y-%m-%d")

                        newHouse.last_updated_home = fixed_date

                        # assign latitude and longitude if they exist
                        try:
                            newHouse.lat = lat
                        except NameError:
                            print("No lat for " + row[0])

                        try:
                            newHouse.lon = lng
                        except NameError:
                            print("No lon for " + row[0])

                        newHouse.air_conditioning = True if row[9].lower() in {'yes', '1', 'true'} else False
                        newHouse.wash_dryer_in_home = True if row[10].lower() in {'yes', '1', 'true'} else False
                        newHouse.dish_washer = True if row[11].lower() in {'yes', '1', 'true'} else False
                        newHouse.bath = True if row[12].lower() in {'yes', '1', 'true'} else False
                        newHouse.num_bedrooms = int(row[5])
                        newHouse.num_bathrooms = int(row[6])
                        newHouse.parking_spot = True if row[13].lower() in {'yes', '1', 'true'} else False
                        newHouse.washer_dryer_in_building = True if row[14].lower() in {'yes', '1', 'true'} else False
                        newHouse.elevator = True if row[15].lower() in {'yes', '1', 'true'} else False
                        newHouse.handicap_access = True if row[16].lower() in {'yes', '1', 'true'} else False
                        newHouse.pool_hot_tub = True if row[17].lower() in {'yes', '1', 'true'} else False
                        newHouse.fitness_center = True if row[18].lower() in {'yes', '1', 'true'} else False
                        newHouse.storage_unit = True if row[19].lower() in {'yes', '1', 'true'} else False

                        newHouse.save()

                        newPhotos = HousePhotosModel(house=newHouse)
                        newPhotos.save()
                        newHouse.save()

                        # Num Bathrooms should be added appropriately
                        # Prints for testing purposes
                        # print(row[0])
                        # print("\n")

            csvfile.close()


