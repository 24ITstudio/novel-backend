

from rest_framework import viewsets
from .models import NUser
from .serializers import NUserSerializer


class NUserViewSet(viewsets.ModelViewSet):
    queryset = NUser.objects.all()
    serializer_class = NUserSerializer
