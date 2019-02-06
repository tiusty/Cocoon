# Import Rest Framework modules
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

# Import Cocoon Modules
from cocoon.houseDatabase.serializers import HomeTypeSerializer
from cocoon.houseDatabase.models import HomeTypeModel


class HomeTypeViewSet(viewsets.ModelViewSet):
    """
    Returns all the home types available to select
    """
    queryset = HomeTypeModel.objects.all()
    serializer_class = HomeTypeSerializer
    permission_classes = [AllowAny]

