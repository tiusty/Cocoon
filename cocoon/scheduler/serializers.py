from rest_framework import serializers

from cocoon.scheduler.models import ItineraryModel
from cocoon.userAuth.models import MyUser


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = MyUser
        fields = ('id', 'email')


class ItinerarySerializer(serializers.HyperlinkedModelSerializer):

    client = UserSerializer(read_only=True)

    class Meta:
        model = ItineraryModel
        fields = ('id', 'client')
