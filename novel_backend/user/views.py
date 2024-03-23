

from rest_framework import viewsets, permissions, status, generics
from rest_framework.mixins import CreateModelMixin
from .models import NUser
from .serializers import NUserSerializer
from novel.models import Novel
from rest_framework.response import Response

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # always allow GET, HEAD, OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.id == request.user.id


class NUserViewSet(viewsets.ModelViewSet):
    queryset = NUser.objects.all()
    serializer_class = NUserSerializer
    permission_classes = (IsOwnerOrReadOnly,)



class CreateNUserSet(CreateModelMixin, viewsets.GenericViewSet):
    queryset = NUser.objects.all()
    serializer_class = NUserSerializer



class FavorNUserSet(generics.CreateAPIView, generics.DestroyAPIView):#CreateModelMixin, DestroyModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsOwner,)

    def create(self, request, pk=None):
        "add user's favors novel, `pk` is novel id"
        if pk is None:
            return Response(dict(detail="arg missed"), status=status.HTTP_400_BAD_REQUEST)
        id = request.user.id
        if id is None:
            return Response(dict(detail="you don't have permission"), status=status.HTTP_400_BAD_REQUEST)
        else:
            novel = Novel.objects.filter(id=pk).first()
            if novel is None:
                return Response(dict(detail="novel with given id not found"), status=status.HTTP_404_NOT_FOUND)

            nuser = NUser.objects.get(id=id)
            nuser.favors.add(novel)
            nuser.save()
            return Response(data=dict(), status=status.HTTP_201_CREATED)

    def destroy(self, request, pk):   #remove user's favors novel
        iduser = request.user.id
        if iduser is None:
            return Response(dict(detail="you don't have permission"), status=status.HTTP_400_BAD_REQUEST)
        else:
            nuser = NUser.objects.get(id=iduser)
            novel = Novel.objects.filter(id=pk).first()
            nuser.favors.remove(novel)
            nuser.save()
            return Response(data=dict(), status=status.HTTP_204_NO_CONTENT)







