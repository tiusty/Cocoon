# Import DRF modules
from rest_framework import serializers

# Import App modules
from .models import ItineraryModel

# Import Third party modules
from cocoon.userAuth.serializers import MyUserSerializer
from cocoon.houseDatabase.serializers import RentDatabaseSerializer


class ItinerarySerializer(serializers.HyperlinkedModelSerializer):

    client = MyUserSerializer(read_only=True)
    agent = MyUserSerializer(read_only=True)
    homes = RentDatabaseSerializer(read_only=True, many=True)

    class Meta:
        model = ItineraryModel
        fields = ('id', 'client', 'itinerary', 'agent', 'tour_duration_seconds', 'selected_start_time', 'homes',
                  'is_claimed', 'is_scheduled')