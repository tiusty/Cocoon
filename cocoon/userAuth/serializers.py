# Import DRF modules
from rest_framework import serializers

# Import App modules
from .models import MyUser


class MyUserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = MyUser
        fields = ('id', 'email', 'full_name', 'phone_number')
