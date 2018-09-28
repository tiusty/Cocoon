# Django modules
from django.test import TestCase
from django.utils import timezone

# Cocoon modules
from cocoon.houseDatabase.models import RentDatabaseModel, HomeTypeModel, HomeProviderModel

# Third party modules
from decimal import Decimal


class TestUpdateFunction(TestCase):

    def setUp(self):
        self.home_type = HomeTypeModel.objects.create(home_type='House')
        self.home_type1 = HomeTypeModel.objects.create(home_type='Apartment')
        HomeProviderModel.objects.create(provider="MLSPIN")
        HomeProviderModel.objects.create(provider="YGL")

    @staticmethod
    def create_destination(home_type, price=1500,
                           currently_available=True, num_bedrooms=2, num_bathrooms=2, zip_code="02476", state="MA"):
        return RentDatabaseModel.objects.create(
            home_type=home_type,
            price=price,
            currently_available=currently_available,
            num_bedrooms=num_bedrooms,
            num_bathrooms=num_bathrooms,
            zip_code=zip_code,
            state=state,
            listing_provider=HomeProviderModel.objects.get(provider="MLSPIN"),
        )

    def test_valid_update(self):
        # Arrange
        # Create a home and save it
        dest = RentDatabaseModel(
            apartment_number='1r',
            street_address='12 Stony Brook Rd',
            city='Arlington',
            state='MA',
            zip_code='02476',
            latitude=25.25,
            longitude=24.24,
            num_bathrooms=2,
            num_bedrooms=1,
            parking_spot=True,
            remarks="hi",
            listing_number='123',
            listing_provider=HomeProviderModel.objects.get(provider="MLSPIN"),
            listing_agent='The agent',
            listing_office='The office',
            last_updated=timezone.now(),
            price=2000,
            home_type=self.home_type,
            currently_available=True,
        )
        dest.save()
        dest_id = dest.id

        # Create another home to update the old home with
        dest1 = RentDatabaseModel(
            apartment_number='3f',
            street_address='360 Huntington Ave',
            city='Boston',
            state='RI',
            zip_code='02474',
            latitude=23.23,
            longitude=22.22,
            num_bathrooms=3,
            num_bedrooms=2,
            parking_spot=False,
            remarks="the",
            listing_number='456',
            listing_provider=HomeProviderModel.objects.get(provider="YGL"),
            listing_agent='The agent 2',
            listing_office='The office 2',
            last_updated=timezone.now() + timezone.timedelta(days=1),
            price=2400,
            home_type=self.home_type1,
            currently_available=False,
        )

        # Act
        # call the update function
        dest.update(dest1)
        dest.save()

        # Assert values of dest in database
        home = RentDatabaseModel.objects.get(id=dest_id)
        # Make sure the update function does not create a new model
        self.assertEqual(RentDatabaseModel.objects.count(), 1)

        # Asserts that every field can be updated
        self.assertEqual(home.apartment_number, '3f')
        self.assertEqual(home.street_address, '360 Huntington Ave')
        self.assertEqual(home.city, 'Boston')
        self.assertEqual(home.state, 'RI')
        self.assertEqual(home.zip_code, '02474')
        self.assertAlmostEquals(home.latitude, Decimal(23.23))
        self.assertAlmostEquals(home.longitude, Decimal(22.22))
        self.assertEqual(home.num_bathrooms, 3)
        self.assertEqual(home.num_bedrooms, 2)
        self.assertFalse(home.parking_spot)
        self.assertEqual(home.remarks, 'the')
        self.assertEqual(home.listing_number, 456)
        self.assertEqual(home.listing_provider, HomeProviderModel.objects.get(provider="YGL"))
        self.assertEqual(home.listing_agent, 'The agent 2')
        self.assertEqual(home.listing_office, 'The office 2')
        self.assertEqual(home.last_updated, (timezone.now() + timezone.timedelta(days=1)).date())
        self.assertEqual(home.price, 2400)
        self.assertEqual(home.home_type, self.home_type1)
        self.assertFalse(home.currently_available)
