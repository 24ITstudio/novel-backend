

from django.shortcuts import get_object_or_404
from django.db.models import Count, F
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.filters import SearchFilter


from .models import Novel,Chapter
from .serializers import NovelSerializer,ChapterSerializer


class _RONovelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Novel.objects.all()
    serializer_class = NovelSerializer


# TODO: remove this, it's deprcated. use `/novel-tag` router instead.
class _Filter(SearchFilter):
    def get_search_fields(self, view, request):
        if request.query_params.get('tag') is not None:
            return ['tag']  
            # if `?tag&search=`, then search on tag
        return super().get_search_fields(view, request)  # seach on name


class NovelViewSet(viewsets.ModelViewSet):
    queryset = Novel.objects.all()
    serializer_class = NovelSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = [_Filter]  # TODO: use `[SearchFilter]` instead, see `_Filter`
    search_fields = ['name']
    # support search via `?search=`
    # ref https://www.django-rest-framework.org/api-guide/filtering/#searchfilter
    
    def retrieve(self, request, *args, **kwargs):
        arg: str = kwargs['pk']
        idx = arg.find('-')
        if idx == -1:
            return super().retrieve(request, *args, **kwargs)
        novel_ord = arg[:idx]
        chapter_ord = arg[idx + 1:]

        novel_queryset = self.queryset
        novel = get_object_or_404(novel_queryset, pk=novel_ord)
        chapter = novel.chapters.filter(chapter_ord=chapter_ord).first()
        if chapter is None:
            return Response(data={"detail": "chapter not found"}, status=404)
        content = chapter.content
        return Response(data=dict(content=content))


class TagViewSet(_RONovelViewSet):
    _target_fields = 'tag'
    filter_backends = [SearchFilter]
    search_fields = [_target_fields]
    def list(self, request):
        if not request.query_params:  # if no `?search=` is given.
            # returns an array of tag
            queryset = Novel.objects.values_list(self._target_fields, flat=True).distinct()
            return Response(data=queryset)
        return super().list(request)


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


class ChaptersViewSet(viewsets.ModelViewSet):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer
    permission_classes = (permissions.IsAuthenticated,)
