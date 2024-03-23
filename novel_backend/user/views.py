

from rest_framework import viewsets, permissions,status
from rest_framework.mixins import CreateModelMixin
from .models import NUser
from .serializers import NUserSerializer
from novel.models import Novel
from rest_framework.response import Response


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


 class FavorNUserSet(viewsets.ModelViewSet):
    queryset = NUser.objects.all()
    serializer_class = NUserSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def create(self,request):   #add user's favors novel
        data = Novel.id
        id = request.user.id
        if id is None:
            return Response(dict(detail="you don't have permission"), status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = self.get_serializer(request.data)
            nuser = NUser.objects.filter(id=id).first()
            nuser.favors.add(data)
            nuser.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk):   #remove user's favors novel
        iduser = request.user.id
        novel = Novel.id
        nuser = NUser.objects.filter(id=iduser).first()
        if nuser is None:
            return Response(dict(detail="you don't have permission"), status=status.HTTP_400_BAD_REQUEST)
        else:
            nuser.favors.remove(novel)
            nuser.save()
            return Response(status=self.HTTP_204_NOT_CONNECTED)





