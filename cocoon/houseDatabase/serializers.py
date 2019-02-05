# Import DRF modules
from rest_framework import serializers

# Import App modules
from .models import RentDatabaseModel, HomeTypeModel, HousePhotos


class HomeImageSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = HousePhotos
        fields = ('id', 'image')


class HomeTypeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = HomeTypeModel
        fields = ('id', 'home_type')


class RentDatabaseSerializer(serializers.HyperlinkedModelSerializer):
    interior_amenities = serializers.SerializerMethodField(read_only=True)
    exterior_amenities = serializers.SerializerMethodField(read_only=True)
    nearby_amenities = serializers.SerializerMethodField(read_only=True)
    home_type = HomeTypeSerializer(read_only=True)
    images = HomeImageSerializer(read_only=True, many=True)

    @staticmethod
    def get_interior_amenities(obj):
        """
        Returns all the interior amenities so it is grouped in the serializer.

        All the data here will be returned in a interior_amenities dictionary
        :param obj: (RentDatabaseModel) -> The rent database model associated with the serializer
        :return: (dict) -> The dictionary for the interior amenities field
        """
        return {
            'furnished': obj.furnished,
            'hardwood_floors': obj.hardwood_floors,
            'air_conditioning': obj.air_conditioning,
            'laundry_in_unit': obj.laundry_in_unit,
            'dishwasher': obj.dishwasher,
        }

    @staticmethod
    def get_exterior_amenities(obj):
        """
        Returns all the exterior amenities so it is grouped in the serializer.

        All the data here will be returned in a exterior_amenities dictionary
        :param obj: (RentDatabaseModel) -> The rent database model associated with the serializer
        :return: (dict) -> The dictionary for the exterior amenities field
        """
        return {
            'pool': obj.pool,
            'patio/balcony': obj.patio_balcony,
            'gym': obj.gym,
            'laundry_in_building': obj.laundry_in_building,
            'storage': obj.storage,
        }

    @staticmethod
    def get_nearby_amenities(obj):
        """
        Returns all the nearby amenities so it is grouped in the serializer.

        All the data here will be returned in a nearby_amenities dictionary
        :param obj: (RentDatabaseModel) -> The rent database model associated with the serializer
        :return: (dict) -> The dictionary for the nearby amenities field
        """
        return {
            'laundromat_nearby': obj.laundromat_nearby
        }

    class Meta:
        model = RentDatabaseModel
        fields = ('id', 'price', 'home_type', 'images', 'remarks', 'num_bedrooms', 'num_bathrooms',
                  'interior_amenities', 'exterior_amenities', 'nearby_amenities',
                  'latitude', 'longitude')


class RentDatabaseSerializerBroker(serializers.HyperlinkedModelSerializer):
    """
    This serializer is meant for broker account becomes it also returns info regarding the listing
    """
    interior_amenities = serializers.SerializerMethodField(read_only=True)
    exterior_amenities = serializers.SerializerMethodField(read_only=True)
    nearby_amenities = serializers.SerializerMethodField(read_only=True)
    broker_info = serializers.SerializerMethodField(read_only=True)
    home_type = HomeTypeSerializer(read_only=True)
    images = HomeImageSerializer(read_only=True, many=True)

    @staticmethod
    def get_broker_info(obj):
        return {
            'full_address': obj.full_address,
            'listing_number': obj.listing_number,
            'listing_agent': obj.listing_agent,
            'listing_office': obj.listing_office,
            'listing_provider': obj.listing_provider.provider
        }

    @staticmethod
    def get_interior_amenities(obj):
        """
        Returns all the interior amenities so it is grouped in the serializer.

        All the data here will be returned in a interior_amenities dictionary
        :param obj: (RentDatabaseModel) -> The rent database model associated with the serializer
        :return: (dict) -> The dictionary for the interior amenities field
        """
        return {
            'furnished': obj.furnished,
            'hardwood_floors': obj.hardwood_floors,
            'air_conditioning': obj.air_conditioning,
            'laundry_in_unit': obj.laundry_in_unit,
            'dishwasher': obj.dishwasher,
        }

    @staticmethod
    def get_exterior_amenities(obj):
        """
        Returns all the exterior amenities so it is grouped in the serializer.

        All the data here will be returned in a exterior_amenities dictionary
        :param obj: (RentDatabaseModel) -> The rent database model associated with the serializer
        :return: (dict) -> The dictionary for the exterior amenities field
        """
        return {
            'pool': obj.pool,
            'patio/balcony': obj.patio_balcony,
            'gym': obj.gym,
            'laundry_in_building': obj.laundry_in_building,
            'storage': obj.storage,
        }

    @staticmethod
    def get_nearby_amenities(obj):
        """
        Returns all the nearby amenities so it is grouped in the serializer.

        All the data here will be returned in a nearby_amenities dictionary
        :param obj: (RentDatabaseModel) -> The rent database model associated with the serializer
        :return: (dict) -> The dictionary for the nearby amenities field
        """
        return {
            'laundromat_nearby': obj.laundromat_nearby
        }

    class Meta:
        model = RentDatabaseModel
        fields = ('id', 'price', 'home_type', 'images', 'remarks', 'num_bedrooms', 'num_bathrooms',
                  'interior_amenities', 'exterior_amenities', 'nearby_amenities', 'broker_info',
                  'latitude', 'longitude')
