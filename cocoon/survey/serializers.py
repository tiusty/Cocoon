from rest_framework import serializers

from cocoon.survey.models import RentingSurveyModel
from cocoon.houseDatabase.models import RentDatabaseModel, HomeTypeModel


class HomeTypeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = HomeTypeModel
        fields = ('home_type',)


class FavoritesSerializer(serializers.HyperlinkedModelSerializer):
    home_type = HomeTypeSerializer(read_only=True)

    class Meta:
        model = RentDatabaseModel
        fields = ('id', 'street_address', 'price', 'home_type')


class VisitListSerializer(serializers.HyperlinkedModelSerializer):
    home_type = HomeTypeSerializer(read_only=True)

    class Meta:
        model = RentDatabaseModel
        fields = ('id', 'price', 'home_type')


class RentSurveySerializer(serializers.HyperlinkedModelSerializer):

    favorites = FavoritesSerializer(read_only=True, many=True)
    visit_list = VisitListSerializer(read_only=True, many=True)

    class Meta:
        model = RentingSurveyModel
        fields = ('id', 'name', 'visit_list', 'favorites', 'url')
