# Import DRF modules
from rest_framework import serializers

# Import App modules
from .models import ItineraryModel
from .models import TimeModel

# Import Third party modules
from cocoon.userAuth.serializers import MyUserSerializer
from cocoon.houseDatabase.serializers import RentDatabaseSerializer


class TimeModelSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = TimeModel
        fields = ('id', 'time', 'time_available_seconds')


class ItinerarySerializer(serializers.HyperlinkedModelSerializer):

    client = MyUserSerializer(read_only=True)
    agent = MyUserSerializer(read_only=True)
    homes = RentDatabaseSerializer(read_only=True, many=True)
    start_times = TimeModelSerializer(read_only=True, many=True)

    class Meta:
        model = ItineraryModel
        fields = ('id', 'client', 'itinerary', 'agent', 'tour_duration_seconds_rounded',
                  'tour_duration_seconds', 'selected_start_time', 'homes',
                  'is_claimed', 'is_scheduled', 'start_times', 'is_pending', 'finished', 'hash')
