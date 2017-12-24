from django.test import TestCase
import datetime

from houseDatabase.models import RentDatabase, ZipCodeDictionary, ZipCodeDictionaryChild
from django.db import IntegrityError

# Defaults for the house database
default_address = "12 Stony Brook Rd"
default_city = "Arlington"
default_state = "MA"
default_zip_code = "02476"
default_price = 700
default_home_type = "Condo"
default_move_in_day = datetime.date.today() + datetime.timedelta(days=10)
default_lon = 71.161418
default_lat = 42.413845
default_air_conditioning = True
default_wash_dryer_in_home = False
default_dish_washer = True
default_bath = False
default_num_bathrooms = 4
default_num_bedrooms = 2
default_parking_spot = False
default_washer_dryer_in_building = False
default_elevator = True
default_handicap_access = False
default_pool_hot_tub = False
default_fitness_center = False
default_storage_unit = True

# defaults for the ZipCodeDictionary
default_ZipCodeDictionary_zip_code = "02476"
default_ZipCodeDictionaryChild_zip_code = "02474"
default_ZipCodeDictionaryChild_commute_time_seconds = 1200
default_ZipCodeDictionaryChild_commute_distance_meters = 25
default_ZipCodeDictionaryChild_commute_type = "driving"


def create_home(address=default_address,
                city=default_city,
                state=default_state,
                zip_code=default_zip_code,
                price=default_price,
                home_type=default_home_type,
                move_in_day=default_move_in_day,
                lon=default_lon,
                lat=default_lat,
                air_conditioning=default_air_conditioning,
                wash_dryer_in_home=default_wash_dryer_in_home,
                dish_washer=default_dish_washer,
                bath=default_bath,
                num_bathrooms=default_num_bathrooms,
                num_bedrooms=default_num_bedrooms,
                parking_spot=default_parking_spot,
                washer_dryer_in_building=default_washer_dryer_in_building,
                elevator=default_elevator,
                handicap_access=default_handicap_access,
                pool_hot_tub=default_pool_hot_tub,
                fitness_center=default_fitness_center,
                storage_unit=default_storage_unit,
                ):
    """
    Creates a home for the testing module.
    Uses default values unless it is passed an argument
    """
    return RentDatabase.objects.create(
        address=address,
        city=city,
        state=state,
        zip_code=zip_code,
        price=price,
        home_type=home_type,
        move_in_day=move_in_day,
        lon=lon,
        lat=lat,
        air_conditioning=air_conditioning,
        wash_dryer_in_home=wash_dryer_in_home,
        dish_washer=dish_washer,
        bath=bath,
        num_bathrooms=num_bathrooms,
        num_bedrooms=num_bedrooms,
        parking_spot=parking_spot,
        washer_dryer_in_building=washer_dryer_in_building,
        elevator=elevator,
        handicap_access=handicap_access,
        pool_hot_tub=pool_hot_tub,
        fitness_center=fitness_center,
        storage_unit=storage_unit,
    )


def create_zip_code_dictionary(
        zip_code=default_ZipCodeDictionary_zip_code
        ):
    return ZipCodeDictionary.objects.create(
        zip_code=zip_code
    )


def create_zip_code_dictionary_with_child(
        zip_code=default_ZipCodeDictionaryChild_zip_code,
        commute_time=default_ZipCodeDictionaryChild_commute_time_seconds,
        commute_distance=default_ZipCodeDictionaryChild_commute_distance_meters,
        commute_type=default_ZipCodeDictionaryChild_commute_type
    ):
    zip_code_dictionary = create_zip_code_dictionary()
    zip_code_dictionary.zipcodedictionarychild_set.create(
        zip_code=zip_code,
        commute_time=commute_time,
        commute_distance=commute_distance,
        commute_type=commute_type,
    )
    return zip_code_dictionary


class ZipCodeDictionaryTestCase(TestCase):

    @staticmethod
    def test_all_model_getters():
        """
        Test all teh getters associated with the ZipCodeDictionary model
        :return:
        """
        zip_code_dictionary = create_zip_code_dictionary_with_child()
        assert(zip_code_dictionary.zip_code() == default_ZipCodeDictionary_zip_code)
        assert(zip_code_dictionary.zipcodedictionarychild_set.get(
            zip_code=default_ZipCodeDictionaryChild_zip_code).zip_code()
               == default_ZipCodeDictionaryChild_zip_code
        )
        assert (zip_code_dictionary.zipcodedictionarychild_set.get(
            zip_code=default_ZipCodeDictionaryChild_zip_code).get_base_zip_code()
                == zip_code_dictionary
                )
        assert(zip_code_dictionary.zipcodedictionarychild_set.get(
            zip_code=default_ZipCodeDictionaryChild_zip_code).get_commute_distance_meters()
               == default_ZipCodeDictionaryChild_commute_distance_meters
        )
        assert (zip_code_dictionary.zipcodedictionarychild_set.get(
            zip_code=default_ZipCodeDictionaryChild_zip_code).get_commute_time_seconds()
                == default_ZipCodeDictionaryChild_commute_time_seconds
                )
        assert (zip_code_dictionary.zipcodedictionarychild_set.get(
            zip_code=default_ZipCodeDictionaryChild_zip_code).get_commute_type()
                == default_ZipCodeDictionaryChild_commute_type
                )

    @staticmethod
    def test_zip_code_dictionary_unique_attribute_same():
            create_zip_code_dictionary()
            try:
                create_zip_code_dictionary()
                raise Exception("ZipCodeDictionary should be unique")
            except IntegrityError:
                pass

    @staticmethod
    def test_zip_code_dictionary_unique_attribute_different():
        create_zip_code_dictionary()
        try:
            create_zip_code_dictionary(zip_code="02474")
        except IntegrityError:
            raise Exception("Integrity Error should not have been raised")


