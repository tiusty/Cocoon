from django.test import TestCase
import datetime

from houseDatabase.models import RentDatabase

default_address = "12 Stony Brook Rd"
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


def create_home(address=default_address,
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


class HouseDataBaseGetters(TestCase):

    def test_all_model_getters(self):
        home = create_home()
        assert(home.get_address() == default_address)
        assert(home.get_price() == default_price)
        assert(home.get_price_str() == "$" + str(home.get_price()))
        assert(home.get_move_in_day() == default_move_in_day)
        assert(home.get_num_bedrooms() == default_num_bedrooms)
        assert(home.get_num_bathrooms() == default_num_bathrooms)
        assert(home.get_home_type() == default_home_type)
        assert(home.get_air_conditioning() == default_air_conditioning)
        assert(home.get_wash_dryer_in_home() == default_wash_dryer_in_home)
        assert(home.get_dish_washer() == default_dish_washer)
        assert(home.get_bath() == default_bath)
        assert(home.get_lat() == default_lat)
        assert(home.get_lon() == default_lon)
        assert(home.get_parking_spot() == default_parking_spot)
        assert(home.get_washer_dryer_in_building() == default_washer_dryer_in_building)
        assert(home.get_elevator() == default_elevator)
        assert(home.get_handicap_access() == default_handicap_access)
        assert(home.get_pool_hot_tub() == default_pool_hot_tub)
        assert(home.get_fitness_center() == default_fitness_center)
        assert(home.get_storage_unit() == default_storage_unit)
