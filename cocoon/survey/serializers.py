# Import DRF modules
from rest_framework import serializers

# Import App modules
from .models import RentingSurveyModel

# Import Third party modules
from cocoon.houseDatabase.serializers import RentDatabaseSerializer


class RentSurveySerializer(serializers.HyperlinkedModelSerializer):

    favorites = RentDatabaseSerializer(read_only=True, many=True)
    visit_list = RentDatabaseSerializer(read_only=True, many=True)

    class Meta:
        model = RentingSurveyModel
        fields = ('id', 'name', 'visit_list', 'favorites', 'url', 'desired_price', 'num_bedrooms')


class HomeScoreSerializer(serializers.Serializer):
    home = RentDatabaseSerializer(read_only=True)
    accumulated_points = serializers.IntegerField()
    total_possible_points = serializers.IntegerField()
