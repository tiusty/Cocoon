from rest_framework import serializers

from cocoon.commutes.models import CommuteType


class CommuteTypeSerializer(serializers.HyperlinkedModelSerializer):

    commute_type = serializers.SerializerMethodField()

    @staticmethod
    def get_commute_type(obj):
        return obj.get_commute_type_display()

    class Meta:
        model = CommuteType
        fields = ('id', 'commute_type')
