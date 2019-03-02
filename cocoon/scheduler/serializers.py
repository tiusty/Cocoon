# Import DRF modules
from rest_framework import serializers

# Import App modules
from .models import ItineraryModel
from .models import TimeModel

# Import Third party modules
from cocoon.userAuth.serializers import MyUserSerializer
from cocoon.houseDatabase.serializers import RentDatabaseSerializer, RentDatabaseSerializerBroker


class TimeModelSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = TimeModel
        fields = ('id', 'time', 'time_available_seconds')


class ItinerarySerializer(serializers.HyperlinkedModelSerializer):

    client = MyUserSerializer(read_only=True)
    agent = MyUserSerializer(read_only=True)
    homes = serializers.SerializerMethodField(read_only=True)
    start_times = TimeModelSerializer(read_only=True, many=True)

    def get_homes(self, obj):
        """
        If the user is a broker or admin they get more info regarding the home
        :param obj:
        :return:
        """
        homes = obj.homes.all()
        if 'user' in self.context:
            user = self.context['user']
            if user.is_broker or user.is_admin:
                return RentDatabaseSerializerBroker(homes, read_only=True, many=True).data

        return RentDatabaseSerializer(homes, read_only=True, many=True).data

    class Meta:
        model = ItineraryModel
        fields = ('id', 'client', 'itinerary', 'agent', 'tour_duration_seconds_rounded',
                  'tour_duration_seconds', 'selected_start_time', 'homes',
                  'is_claimed', 'is_scheduled', 'start_times', 'is_pending', 'finished', 'hash',
                  'itinerary', 'url')
