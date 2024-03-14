

from rest_framework import viewsets, permissions
from rest_framework.mixins import CreateModelMixin
from .models import NUser
from .serializers import NUserSerializer

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # always allow GET, HEAD, OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.username == request.user.username

class NUserViewSet(viewsets.ModelViewSet):
    queryset = NUser.objects.all()
    serializer_class = NUserSerializer
    permission_classes = IsOwnerOrReadOnly,#(permissions.IsAuthenticatedOrReadOnly,)

    def create(self, validated_data):
        return NUser.objects.create_user(**validated_data)

class CreateNUserSet(CreateModelMixin, viewsets.GenericViewSet):
    queryset = NUser.objects.all()
    serializer_class = NUserSerializer
