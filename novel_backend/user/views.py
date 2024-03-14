

from rest_framework import viewsets, permissions
from rest_framework.mixins import CreateModelMixin
from .models import NUser
from .serializers import NUserSerializer


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # always allow GET, HEAD, OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True
        # It's ensured that username is unique
        return obj.username == request.user.username


class NUserViewSet(viewsets.ModelViewSet):
    queryset = NUser.objects.all()
    serializer_class = NUserSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def create(self, validated_data):
        # This makes sure password is encrypted
        return NUser.objects.create_user(**validated_data)


class CreateNUserSet(CreateModelMixin, viewsets.GenericViewSet):
    queryset = NUser.objects.all()
    serializer_class = NUserSerializer
