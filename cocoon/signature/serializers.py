# Import DRF modules
from rest_framework import serializers

# Import App modules
from .models import HunterDocManagerModel, HunterDocModel, HunterDocTemplateModel


class HunterDocTemplateSerializer(serializers.HyperlinkedModelSerializer):

    template_type = serializers.SerializerMethodField()

    @staticmethod
    def get_template_type(obj):
        return obj.get_template_type_display()

    class Meta:
        model = HunterDocTemplateModel
        fields = ('id', 'template_type')


class HunterDocSerializer(serializers.HyperlinkedModelSerializer):

    template = HunterDocTemplateSerializer(read_only=True)

    class Meta:
        model = HunterDocModel
        fields = ('id', 'template', 'is_signed')


class HunterDocManagerSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = HunterDocManagerModel
        fields = ('id', 'is_all_documents_signed', 'is_pre_tour_signed')
