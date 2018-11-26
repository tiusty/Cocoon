from rest_framework import serializers

from cocoon.houseDatabase.models import HomeTypeModel


class HomeTypeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = HomeTypeModel
        fields = ('id', 'home_type')
