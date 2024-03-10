
from rest_framework import viewsets
from .models import Novel
from .serializers import NovelSerializer

class NovelViewSet(viewsets.ModelViewSet):
    queryset = Novel.objects.all()
    serializer_class = NovelSerializer
