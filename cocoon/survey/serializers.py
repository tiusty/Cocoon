from rest_framework import serializers

from cocoon.survey.models import RentingSurveyModel
from cocoon.houseDatabase.models import RentDatabaseModel


class FavoritesSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = RentDatabaseModel
        fields = ('id', 'street_address')


class VisitListSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = RentDatabaseModel
        fields = ('id',)


class RentSurveySerializer(serializers.HyperlinkedModelSerializer):

    favorites = FavoritesSerializer(read_only=True, many=True)
    visit_list = VisitListSerializer(read_only=True, many=True)

    class Meta:
        model = RentingSurveyModel
        fields = ('id', 'name', 'visit_list', 'favorites')
