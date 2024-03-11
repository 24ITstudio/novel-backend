from django.test import TestCase

# ref https://docs.djangoproject.com/zh-hans/4.2/topics/testing/overview/

from rest_framework.test import APIRequestFactory
from .views import NovelViewSet, HotNovelViewSet
from .models import Novel, Chapter
from user.models import NUser, Novel


F_NAME = "the first one"
F_F_CONTENT = "Content"
MAX_FAV_NAME = "the mostly favor-ed"

class ApiTestCase(TestCase):
    def setUp(self):
        n1 = Novel.objects.create(name=F_NAME, desc="desc", max_chapter=1)
        c1 = Chapter.objects.create(novel=n1,  chapter_ord=1, content=F_F_CONTENT)

        nuser = NUser.objects.create()
        nuser.save()  # must save before `add`
        Novel.objects.create(name="non-favor", desc="Desc", max_chapter=3)
        fav = Novel.objects.create(name=MAX_FAV_NAME, desc="Desc", max_chapter=3)
        nuser.favors.add(fav)

    def test_novel_get_and_post(self):
        # test status code and data
        factory = APIRequestFactory()

        def t_get(url, pk=None, get_method='list'):
            request = factory.get(url)
            response = NovelViewSet.as_view({'get': get_method})(request, pk=pk)
            self.assertEqual(response.status_code, 200)
            return response.data
        t_get('/novel/')
        n1 = t_get('/novel/1',  "1",  'retrieve')
        self.assertEqual(n1['name'], F_NAME)
        c1 = t_get('/novel/1-1',"1-1",'retrieve')
        self.assertEqual(c1['content'], F_F_CONTENT)
        # handle POST
        request = factory.post('/novel/', {'name': 'Another book', 'desc': 'Desc', 'max_chapter': 3})
        response = NovelViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 201)
    def test_hotnovel(self):
        factory = APIRequestFactory()
        request = factory.get('/hotnovel/')
        response = HotNovelViewSet.as_view({'get': 'list'})(request)

        self.assertEqual(
            response.data[0]['name'], MAX_FAV_NAME)
