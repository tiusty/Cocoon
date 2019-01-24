# Import DRF modules
from rest_framework import serializers

# Import App modules
from .models import RentingSurveyModel, TenantModel

# Import Third party modules
from cocoon.houseDatabase.serializers import RentDatabaseSerializer
from cocoon.commutes.serializers import CommuteTypeSerializerJustId


class TenantSerializer(serializers.HyperlinkedModelSerializer):
    commute_type = CommuteTypeSerializerJustId()

    class Meta:
        model = TenantModel
        fields = ('first_name', 'last_name', 'id',
                  'street_address', 'city', 'state', 'zip_code',
                  'commute_type', 'commute_weight', 'traffic_option',
                  'min_commute', 'max_commute')


class RentSurveySerializer(serializers.HyperlinkedModelSerializer):
    generalInfo = serializers.SerializerMethodField()
    amenitiesInfo = serializers.SerializerMethodField()
    favorites = RentDatabaseSerializer(read_only=True, many=True)
    visit_list = RentDatabaseSerializer(read_only=True, many=True)
    tenants = TenantSerializer(read_only=True, many=True)

    @staticmethod
    def get_generalInfo(obj):
        """
        Function returns the generalInfo as the frontend expects it
        :param obj: (RentSurveyModel) -> The survey that the data is coming from
        :return: (dict) -> All the fields in the generalInfo field on the frontend
        """
        # Retrieves the ids of all the home types associated with the survey and stores them in a list
        home_type_ids = []
        for home_type in obj.home_type.all():
            home_type_ids.append(home_type.id)
        return {
            'desired_price': obj.desired_price,
            'max_price': obj.max_price,
            'price_weight': obj.price_weight,
            'number_of_tenants': obj.tenants.count(),
            'home_type': home_type_ids,
            'num_bedrooms': obj.num_bedrooms,
            'polygon_filter_type': obj.polygon_filter_type,

            # need to store this in the survey
            'is_move_asap': 'yes',
            'move_weight': 2,
        }

    @staticmethod
    def get_amenitiesInfo(obj):
        """
        Function returns all the amenities info as the frontend would expect it
        :param obj: (RentSurveyModel) -> The survey that the data is coming from
        :return: (dict) -> All the fields in the amenitiesInfo field on the frontend
        """
        return {
            'wants_laundry_in_unit': obj.wants_laundry_in_unit,
            'wants_laundry_in_building': obj.wants_laundry_in_building,
            'wants_laundry_nearby': obj.wants_laundry_nearby,
            'wants_parking': obj.wants_parking,
            'number_of_cars': obj.number_of_cars,
            'wants_furnished': obj.wants_furnished,
            'furnished_weight': obj.furnished_weight,
            'wants_dogs': obj.wants_dogs,
            'number_of_dogs': obj.number_of_dogs,
            'service_dogs': obj.service_dogs,
            'dog_size': obj.dog_size,
            'breed_of_dogs': obj.breed_of_dogs,
            'wants_cats': obj.wants_cats,
            'cat_weight': obj.cat_weight,
            'wants_hardwood_floors': obj.wants_hardwood_floors,
            'hardwood_floors_weight': obj.hardwood_floors_weight,
            'wants_AC': obj.wants_AC,
            'AC_weight': obj.AC_weight,
            'wants_dishwasher': obj.wants_dishwasher,
            'dishwasher_weight': obj.dishwasher_weight,
            'wants_patio': obj.wants_patio,
            'patio_weight': obj.patio_weight,
            'wants_pool': obj.wants_pool,
            'pool_weight': obj.pool_weight,
            'wants_gym': obj.wants_gym,
            'gym_weight': obj.gym_weight,
            'wants_storage': obj.wants_storage,
            'storage_weight': obj.storage_weight,
        }

    class Meta:
        model = RentingSurveyModel
        fields = ('id', 'name', 'visit_list', 'favorites', 'url', 'desired_price', 'num_bedrooms', 'tenants',
                  'generalInfo', 'amenitiesInfo')


class HomeScoreSerializer(serializers.Serializer):
    home = RentDatabaseSerializer(read_only=True)
    percent_match = serializers.IntegerField()
