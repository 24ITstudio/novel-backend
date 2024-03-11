from django.test import TestCase

# ref https://docs.djangoproject.com/zh-hans/4.2/topics/testing/overview/

from rest_framework.test import APIRequestFactory
from .views import NovelViewSet
from .models import Novel, Chapter


class ApiTestCase(TestCase):
    def setUp(self):
        n1 = Novel.objects.create(name="a book", desc="desc", max_chapter=1)
        c1 = Chapter.objects.create(novel=n1,  chapter_ord=1, content="content for test")

    def test_get_and_post(self):
        # current only test status code.
        factory = APIRequestFactory()

        def t_get(url):
            request = factory.get(url)
            response = NovelViewSet.as_view({'get': 'list'})(request)
            self.assertEqual(response.status_code, 200)
        t_get('/novel/')
        t_get('/novel/1')
        t_get('/novel/1-1')
        # handle POST
        request = factory.post('/novel/', {'name': 'Another book', 'desc': 'Desc', 'max_chapter': 3})
        response = NovelViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 201)
