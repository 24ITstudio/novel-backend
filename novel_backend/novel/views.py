

from django.shortcuts import get_object_or_404
from django.db.models import Count, F
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Novel
from .serializers import NovelSerializer

class _RONovelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Novel.objects.all()
    serializer_class = NovelSerializer


class NovelViewSet(_RONovelViewSet, viewsets.ModelViewSet):
    def retrieve(self, request, *args, **kwargs):
        arg: str = kwargs['pk']
        idx = arg.find('-')
        if idx == -1:
          return super().retrieve(request, *args, **kwargs)
        novel_ord = arg[:idx]
        chapter_ord = arg[idx+1:]

        novel_queryset = self.queryset
        novel = get_object_or_404(novel_queryset, pk=novel_ord)
        chapter = novel.chapters.filter(chapter_ord=chapter_ord).first()
        if chapter is None:
            return Response(data={"detail":"chapter not found"}, status=404)
        content = chapter.content
        return Response(data=dict(content=content))


MostHotNovel = 10
class HotNovelViewSet(_RONovelViewSet):
    # get the most `favorite`-ed novels (number limited by `MostHotNovel`)
    queryset = Novel.objects.alias(
        num_favors=Count('nuser')
        ).order_by(F('num_favors').desc())[:MostHotNovel]
    # ref https://docs.djangoproject.com/en/5.0/ref/models/expressions/
    #     https://docs.djangoproject.com/en/5.0/ref/models/querysets/#order-by
    #     https://docs.djangoproject.com/en/5.0/ref/models/querysets/#alias
    #     https://docs.djangoproject.com/en/5.0/topics/db/queries/#limiting-querysets
