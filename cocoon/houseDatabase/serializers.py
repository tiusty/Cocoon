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
    home_type = HomeTypeSerializer(read_only=True)
    images = HomeImageSerializer(read_only=True, many=True)

    class Meta:
        model = RentDatabaseModel
        fields = ('id', 'price', 'home_type', 'images', 'remarks', 'num_bedrooms', 'num_bathrooms', 'latitude', 'longitude',)
