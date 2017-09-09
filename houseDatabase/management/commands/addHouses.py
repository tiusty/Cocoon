import csv
import geocoder
import sys
import os
from django.core.management.base import BaseCommand, CommandError
from houseDatabase.models import HousePhotos, RentDatabase, InteriorAmenities, BuildingExteriorAmenities
from django.utils import timezone

class Command(BaseCommand):
    help = 'Adds listings to database from a specific csv format'

    def add_arguments(self, parser):
         parser.add_argument('file', nargs='+')

    def handle(self, *args, **options):

        for str in options['file']:

            module_dir = os.path.dirname(__file__)  # get current directory
            file_path = os.path.join(module_dir, str)

            csvfile = open(file_path)
            reader = csv.reader(csvfile, delimiter=',')

            '''
            Reference for CSV columns
            
            [0] Address
            [1] Move-in Date
            [2] # Bedrooms
            [3] Home type
            [4] Rent
            [5] AC
            [6] Washer/Dryer
            [7] Dish Washer
            [8] Bath
            [9] Parking Spot
            [10] Washer/Dryer in Building
            [11] Elevator
            [12] Handicap Access
            [13] Pool / Hot Tub
            [14] Fitness Center
            [15] Storage Unit
            
            '''
            for row in reader:


                # g = geocoder.google(row[0])

                # Creating a database object
                # newHouse = RentDatabase
                # newHouse.address = row[0]


                print(row[0])
                print(row[1])
                print("\n")

                ## print(g.latlng)
            csvfile.close()


