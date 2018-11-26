from rest_framework import viewsets

from cocoon.houseDatabase.serializers import HomeTypeSerializer
from cocoon.houseDatabase.models import HomeTypeModel


class HomeTypeViewSet(viewsets.ModelViewSet):
    """
    Returns all the home types available to select
    """
    queryset = HomeTypeModel.objects.all()
    serializer_class = HomeTypeSerializer

