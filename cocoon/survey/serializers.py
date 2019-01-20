# Import DRF modules
from rest_framework import serializers

# Import App modules
from .models import RentingSurveyModel, TenantModel

# Import Third party modules
from cocoon.houseDatabase.serializers import RentDatabaseSerializer


class TenantSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = TenantModel
        fields = ('first_name', 'last_name')


class RentSurveySerializer(serializers.HyperlinkedModelSerializer):

    favorites = RentDatabaseSerializer(read_only=True, many=True)
    visit_list = RentDatabaseSerializer(read_only=True, many=True)
    tenants = TenantSerializer(read_only=True, many=True)

    class Meta:
        model = RentingSurveyModel
        fields = ('id', 'name', 'visit_list', 'favorites', 'url', 'desired_price', 'num_bedrooms', 'tenants')


