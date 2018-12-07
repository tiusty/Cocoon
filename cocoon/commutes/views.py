# Import Rest Framework modules
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

# Import Cocoon Modules
from cocoon.commutes.serializers import CommuteTypeSerializer
from cocoon.commutes.models import CommuteType


class CommuteTypeViewSet(viewsets.ModelViewSet):
    """
    Returns all the commute types available to select
    """
    queryset = CommuteType.objects.all()
    serializer_class = CommuteTypeSerializer
    permission_classes = [AllowAny]
