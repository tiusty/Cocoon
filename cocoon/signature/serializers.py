# Import DRF modules
from rest_framework import serializers

# Import App modules
from .models import HunterDocManagerModel


class HunterDocManagerSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = HunterDocManagerModel
        fields = ('id', 'is_all_documents_signed', 'is_pre_tour_signed')
