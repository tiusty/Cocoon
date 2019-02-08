# Import DRF modules
from rest_framework import serializers

# Import App modules
from .models import RentingSurveyModel, TenantModel

# Import Third party modules
from cocoon.houseDatabase.serializers import RentDatabaseSerializer, RentDatabaseSerializerBroker
from cocoon.commutes.serializers import CommuteTypeSerializerJustId


class TenantSerializer(serializers.HyperlinkedModelSerializer):
    commute_type = CommuteTypeSerializerJustId()

    class Meta:
        model = TenantModel
        fields = ('first_name', 'last_name', 'id',
                  'street_address', 'city', 'state', 'zip_code',
                  'commute_type', 'commute_weight', 'traffic_option',
                  'desired_commute', 'max_commute', 'income', 'credit_score',
                  'occupation', 'other_occupation_reason', 'unemployed_follow_up', 'new_job', 'full_address')


class RentSurveySerializer(serializers.HyperlinkedModelSerializer):
    generalInfo = serializers.SerializerMethodField()
    amenitiesInfo = serializers.SerializerMethodField()
    favorites = serializers.SerializerMethodField()
    visit_list = serializers.SerializerMethodField()
    tenants = TenantSerializer(read_only=True, many=True)

    def get_visit_list(self, obj):
        """
        If the user is a broker or admin they get more info regarding the home
        :param obj:
        :return:
        """
        homes = obj.visit_list.all()
        if 'user' in self.context:
            user = self.context['user']
            if user.is_broker or user.is_admin:
                return RentDatabaseSerializerBroker(homes, read_only=True, many=True).data

        return RentDatabaseSerializer(homes, read_only=True, many=True).data

    def get_favorites(self, obj):
        """
        If the user is a broker or admin they get more info regarding the home
        :param obj:
        :return:
        """
        homes = obj.favorites.all()
        if 'user' in self.context:
            user = self.context['user']
            if user.is_broker or user.is_admin:
                return RentDatabaseSerializerBroker(homes, read_only=True, many=True).data

        return RentDatabaseSerializer(homes, read_only=True, many=True).data

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

        # Converts the polygons from the database version to the frontend version
        polygons = []
        counter = 1
        for polygon in obj.polygons.all():
            vertices = []
            for vertex in polygon.vertices.all():
                vertices.append({
                    'lat': vertex.lat,
                    'lng': vertex.lng,
                })
            polygons.append({
                'key': counter,
                'vertices': vertices,
            })
            counter += 1

        return {
            'desired_price': obj.desired_price,
            'max_price': obj.max_price,
            'price_weight': obj.price_weight,
            'number_of_tenants': obj.tenants.count(),
            'home_type': home_type_ids,
            'num_bedrooms': obj.num_bedrooms,
            'polygon_filter_type': obj.polygon_filter_type,
            'move_weight': obj.move_weight,
            'polygons': polygons,
            'earliest_move_in': obj.earliest_move_in,
            'latest_move_in': obj.latest_move_in,
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
            'laundry_in_unit_weight': obj.laundry_in_unit_weight,
            'wants_laundry_in_building': obj.wants_laundry_in_building,
            'laundry_in_building_weight': obj.laundry_in_building_weight,
            'wants_laundry_nearby': obj.wants_laundry_nearby,
            'laundry_nearby_weight': obj.laundry_nearby_weight,
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
        fields = ('id', 'survey_name', 'visit_list', 'favorites', 'url', 'desired_price', 'num_bedrooms', 'tenants',
                  'generalInfo', 'amenitiesInfo')


class HomeScoreSerializer(serializers.Serializer):
    home = serializers.SerializerMethodField()
    percent_match = serializers.IntegerField()

    def get_home(self, obj):
        """
        If the user is a broker or admin they get more info regarding the home
        :param obj:
        :return:
        """
        if 'user' in self.context:
            user = self.context['user']
            if user.is_broker or user.is_admin:
                return RentDatabaseSerializerBroker(obj.home, read_only=True).data

        return RentDatabaseSerializer(obj.home, read_only=True).data
