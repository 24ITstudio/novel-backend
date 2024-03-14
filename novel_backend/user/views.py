

from rest_framework import viewsets, permissions
from .models import NUser
from .serializers import NUserSerializer


class NUserViewSet(viewsets.ModelViewSet):
    queryset = NUser.objects.all()
    serializer_class = NUserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
