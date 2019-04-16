# Django Imports
from django.utils import timezone
from django.db import IntegrityError
from django.core.exceptions import ValidationError

# Python Imports
from rets import Session
from datetime import datetime, timedelta
from pytz import timezone as pytimezone

# Cocoon Imports
from cocoon.houseDatabase.models import RentDatabaseModel, HomeProviderModel, HomeTypeModel
from cocoon.houseDatabase.management.commands.helpers.word_scraper import WordScraper
from cocoon.houseDatabase.constants import CURRENTLY_AVAILABLE_DELTA_DAYS

# Load the logger
import logging
logger = logging.getLogger(__name__)


class MLSRetsRequester(object):

    QUERY_LIMIT = 3000

    def __init__(self, timestamp):
        self.update_timestamp = timestamp
        login_url = 'http://mlspin-dd.apps.retsiq.com/contact/rets/login'
        username = 'AN5056'
        password = 'izeh6e'
        self.rets_client = Session(login_url, username, password=password, version="RETS/1.8", http_auth='basic')
        self.rets_client.login()

        self.num_houses = 0
        self.num_added_homes = 0
        self.num_of_duplicates = 0
        self.num_of_value_errors = 0
        self.num_failed_to_update = 0
        self.num_updated_homes = 0
        self.num_integrity_errors = 0
        self.num_available_in_future = 0
        self.num_validation_error = 0

    def run(self):
        homes = self.pull_rets_feed()

        for home in homes:
            self.num_houses += 1
            self.add_home_to_database(home)

        manager = HomeProviderModel.objects.get_or_create(provider=HomeProviderModel.MLSPIN)[0]
        manager.last_updated_feed = self.update_timestamp
        manager.save()

        logger.info("\nNumber of houses in database: {0}\n".format(self.num_houses) +
                    "Num added homes: {0}\n".format(self.num_added_homes) +
                    "Num updated homes: {0}\n".format(self.num_updated_homes) +
                    "Update timestamp: {0}\n".format(self.update_timestamp.date()) +
                    "Number of duplicates: {0}\n".format(self.num_of_duplicates) +
                    "Number of value errors: {0}\n".format(self.num_of_value_errors) +
                    "Number of failed updated houses: {0}\n".format(self.num_failed_to_update) +
                    "Number of future homes: {0}\n".format(self.num_available_in_future) +
                    "Number of integrity error is: {0}\n".format(self.num_integrity_errors) +
                    "Number of validation error is: {0}\n".format(self.num_validation_error))

    def pull_rets_feed(self):
        offset = 0
        offset_not_hit = True

        homes = []

        while offset_not_hit:
            search_results = self.rets_client.search(resource='RESI',
                                                     resource_class='RN',
                                                     search_filter=
                                                     {
                                                         'StandardStatus': 'ACT',

                                                     },
                                                     offset=offset,
                                                     limit=self.QUERY_LIMIT)
            homes += search_results
            if len(search_results) == self.QUERY_LIMIT:
                offset += self.QUERY_LIMIT
            else:
                offset_not_hit = False

        return homes

    def add_home_to_database(self, home):
        new_listing = RentDatabaseModel()
        num_of_value_errors = 0

        try:
            # Home Address info
            new_listing.street_address = "{0} {1}".format(home['StreetNumber'], home['StreetName']).replace(',', '')
            new_listing.city = home['City']
            new_listing.state = home['StateOrProvince']
            new_listing.zip_code = home['PostalCode']
            new_listing.latitude = home['Latitude']
            new_listing.longitude = home['Longitude']

            # Home Basic info
            new_listing.price = int(float(home['ListPrice']))
            new_listing.num_bedrooms = int(home['BedroomsTotal'])
            new_listing.num_bathrooms = int(home['BathroomsFull'])
            new_listing.apartment_number = home['UnitNumber']

            # MLS listing information
            new_listing.remarks = home['PublicRemarks']
            new_listing.listing_number = home['ListingId']
            new_listing.listing_agent_id = home['ListAgentMlsId']
            new_listing.listing_office_id = home['ListOfficeMlsId']
            new_listing.listing_provider = HomeProviderModel.objects.get_or_create(provider=HomeProviderModel.MLSPIN)[0]

            # Amenities
            new_listing.dogs_allowed = 'yes' in home['PETS_ALLOWED'].lower()
            new_listing.cats_allowed = 'yes' in home['PETS_ALLOWED'].lower()
            word_scraper_remarks = WordScraper(new_listing.remarks)
            word_scraper_appliances = WordScraper(home['Appliances'])
            new_listing.air_conditioning = home['AIR_CONDITION'] == 'Yes'
            if word_scraper_remarks.look_for_ac() or word_scraper_appliances.look_for_ac():
                new_listing.air_conditioning = True

            new_listing.furnished = word_scraper_remarks.word_finder(["furnished"]) \
                                    or word_scraper_appliances.word_finder(["furnished"])
            new_listing.hardwood_floors = word_scraper_remarks.look_for_hardwood_floors() \
                                          or word_scraper_appliances.look_for_hardwood_floors()
            new_listing.dishwasher = word_scraper_remarks.word_finder(["dishwasher"]) \
                                     or word_scraper_appliances.word_finder(["dishwasher"])
            new_listing.laundry_in_building = word_scraper_remarks.look_for_laundry_in_building() \
                                              or word_scraper_appliances.look_for_laundry_in_building()
            if word_scraper_remarks.word_finder(["pool"]) or word_scraper_remarks.word_finder(["hot","tub"]):
                new_listing.pool = True
            if word_scraper_remarks.word_finder(["balcony"]) or word_scraper_remarks.word_finder(["patio"]):
                new_listing.patio_balcony = True
            new_listing.storage = word_scraper_remarks.word_finder(["storage"])

            new_listing.last_updated = self.update_timestamp

            list_type = home['RN_TYPE']
            if list_type == "Apartment":
                new_listing.home_type = HomeTypeModel.objects.get_or_create(home_type=HomeTypeModel.APARTMENT)[0]
            elif list_type == "Single Family":
                new_listing.home_type = HomeTypeModel.objects.get_or_create(home_type=HomeTypeModel.SINGLE_FAMILY)[0]
            elif list_type == "Condominium":
                new_listing.home_type = HomeTypeModel.objects.get_or_create(home_type=HomeTypeModel.CONDO)[0]
            else:
                new_listing.home_type = HomeTypeModel.objects.get_or_create(home_type=HomeTypeModel.OTHER)[0]

            if home['Date_Available']:
                date_available = datetime.strptime(home['Date_Available'], '%Y-%m-%dT%H:%M:%S')
                new_listing.date_available = date_available
                date_available = pytimezone('US/Eastern').localize(date_available)
                if timezone.now() > date_available - timedelta(days=CURRENTLY_AVAILABLE_DELTA_DAYS):
                    new_listing.currently_available = True
                else:
                    self.num_available_in_future += 1

            else:
                new_listing.currently_available = True

        except ValueError:
            num_of_value_errors += 1
            return

        # Determines if the home already exists as a MLSPIN house
        if RentDatabaseModel.objects \
                .filter(listing_provider=new_listing.listing_provider) \
                .filter(street_address=new_listing.street_address) \
                .filter(city=new_listing.city) \
                .filter(state=new_listing.state) \
                .filter(zip_code=new_listing.zip_code) \
                .filter(apartment_number=new_listing.apartment_number) \
                .exists():

            # Retrieve the home that the home matches
            existing_apartment = RentDatabaseModel.objects.get(
                street_address=new_listing.street_address,
                city=new_listing.city,
                state=new_listing.state,
                zip_code=new_listing.zip_code,
                apartment_number=new_listing.apartment_number
            )

            # Since the apartments are the same
            #   Update the existing apartment with the fields stored in the new listing
            existing_apartment.update(new_listing)
            try:
                existing_apartment.save()
                print("[ UPDATED ] {0}".format(existing_apartment.full_address))
                self.num_updated_homes += 1
            except ValidationError:
                print('Validation error')
                self.num_validation_error += 1

        # Tests if the home exists within another provider
        #   If so mark it as a duplicate and don't add it
        elif RentDatabaseModel.objects \
                .filter(street_address=new_listing.street_address) \
                .filter(city=new_listing.city) \
                .filter(state=new_listing.state) \
                .filter(zip_code=new_listing.zip_code) \
                .filter(apartment_number=new_listing.apartment_number) \
                .exists():
            print("[ DUPLICATE ] {0}".format(new_listing.full_address))
            self.num_of_duplicates += 1
        else:

            try:
                new_listing.save()
                self.num_added_homes += 1
                print("[ ADDING ] " + new_listing.full_address)
            except IntegrityError:
                print("[ Integrity Error ] ")
                self.num_integrity_errors += 1
            except ValidationError:
                print("[ Validation Error ] ")
                self.num_validation_error += 1


