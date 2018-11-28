# Import DRF modules
from rest_framework import serializers

# Import App modules
from .models import HunterDocManagerModel, HunterDocModel


class HunterDocSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = HunterDocModel
        fields = ('id',)


class HunterDocManagerSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = HunterDocManagerModel
        fields = ('id', 'is_all_documents_signed', 'is_pre_tour_signed')
