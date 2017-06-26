from django.test import TestCase

from django.utils import timezone

from survey.forms import RentSurvey
from survey.models import HomeType


# FIX NAMING FOR WASH_dryer_in_home
# Create your tests here.
class SurveyFormTest(TestCase):

    def setUp(self):
        HomeType.objects.create(homeType="Apartment")
        HomeType.objects.create(homeType="Condo")
        HomeType.objects.create(homeType="Town House")
        HomeType.objects.create(homeType="House")
        self.default_min_price = 500
        self.default_max_price = 2000
        self.default_price_weight = 2
        self.default_min_commute = 20
        self.default_max_commute = 90
        self.default_home_type = ['2']
        self.default_commute_weight = 1
        self.default_commute_type = "driving"
        self.default_move_in_date_start = timezone.now() + timezone.timedelta(days=20)
        self.default_move_in_date_end = timezone.now() + timezone.timedelta(days=50)
        self.default_num_bedrooms = 2
        self.default_air_conditioning = 3
        self.default_wash_dryer_in_home = -1
        self.default_dish_washer = 1
        self.default_bath = 1
        self.default_max_bathrooms = 5
        self.default_min_bathrooms = 1
        self.default_parking_spot = 0
        self.default_washer_dryer_in_building = -3
        self.default_elevator = 0
        self.default_handicap_access = 1
        self.default_pool_hot_tub = 0
        self.default_fitness_center = -1
        self.default_storage_unit = -2

    def create_form_rent_survey(self):
        form_data = {
            'min_price': self.default_min_price,
            'max_price': self.default_max_price,
            'price_weight': self.default_price_weight,
            'min_commute': self.default_min_commute,
            'max_commute': self.default_max_commute,
            'home_type': self.default_home_type,
            'commute_weight': self.default_commute_weight,
            'commute_type': self.default_commute_type,
            'move_in_date_start': self.default_move_in_date_start,
            'move_in_date_end': self.default_move_in_date_end,
            'num_bedrooms': self.default_num_bedrooms,
            'air_conditioning': self.default_air_conditioning,
            'wash_dryer_in_home': self.default_wash_dryer_in_home,
            'dish_washer': self.default_dish_washer,
            'bath': self.default_bath,
            'max_bathrooms': self.default_max_bathrooms,
            'min_bathrooms': self.default_min_bathrooms,
            'parking_spot': self.default_parking_spot,
            'washer_dryer_in_building': self.default_washer_dryer_in_building,
            'elevator': self.default_elevator,
            'handicap_access': self.default_handicap_access,
            'pool_hot_tub': self.default_pool_hot_tub,
            'fitness_center': self.default_fitness_center,
            'storage_unit': self.default_storage_unit,
        }
        form = RentSurvey(data=form_data)
        return form

    def test_forms_correct_input(self):
        form = self.create_form_rent_survey()
        print(form.errors)
        self.assertTrue(form.is_valid())

