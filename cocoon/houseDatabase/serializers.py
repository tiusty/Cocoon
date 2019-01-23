# Import DRF modules
from rest_framework import serializers

# Import App modules
from .models import RentDatabaseModel, HomeTypeModel, HousePhotos, HouseInteriorAmenitiesModel


class HomeImageSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = HousePhotos
        fields = ('id', 'image')


class HomeTypeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = HomeTypeModel
        fields = ('id', 'home_type')


class InteriorAmenitiesSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = HouseInteriorAmenitiesModel
        fields = ('furnished',)


class RentDatabaseSerializer(serializers.HyperlinkedModelSerializer):
    interior_amenities = serializers.SerializerMethodField()
    exterior_amenities = serializers.SerializerMethodField()
    nearby_amenities = serializers.SerializerMethodField()
    home_type = HomeTypeSerializer(read_only=True)
    images = HomeImageSerializer(read_only=True, many=True)

    @staticmethod
    def get_interior_amenities(obj):
        return {
            'furnished': obj.furnished,
            'hardwood_floors': obj.hardwood_floors,
            'air_conditioning': obj.air_conditioning,
            'laundry_in_unit': obj.laundry_in_unit,
            'dishwasher': obj.dishwasher,
        }

    @staticmethod
    def get_exterior_amenities(obj):
        return {
            'pool': obj.pool,
            'patio/balcony': obj.patio_balcony,
            'gym': obj.gym,
            'laundry_in_building': obj.laundry_in_building,
            'storage': obj.storage,
        }

    @staticmethod
    def get_nearby_amenities(obj):
        return {
            'laundromat_nearby': obj.laundromat_nearby
        }

    class Meta:
        model = RentDatabaseModel
        fields = ('id', 'price', 'home_type', 'images', 'remarks', 'num_bedrooms', 'num_bathrooms',
                  'interior_amenities', 'exterior_amenities', 'nearby_amenities')
