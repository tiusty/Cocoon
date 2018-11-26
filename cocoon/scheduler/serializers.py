# Import DRF modules
from rest_framework import serializers

# Import App modules
from .models import ItineraryModel

# Import Third party modules
from cocoon.userAuth.serializers import MyUserSerializer


class ItinerarySerializer(serializers.HyperlinkedModelSerializer):

    client = MyUserSerializer(read_only=True)

    class Meta:
        model = ItineraryModel
        fields = ('id', 'client')
