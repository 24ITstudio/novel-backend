from django.test import TestCase
# ref https://docs.djangoproject.com/zh-hans/4.2/topics/testing/overview/

from rest_framework.test import APIRequestFactory
from .views import NUserViewSet
from .models import NUser, Novel


class ApiTestCase(TestCase):
    def setUp(self):
        nuser = NUser.objects.create()
        nuser.save()  # must save before `add`
        Novel.objects.create(name="non-favor", desc="Desc", max_chapter=3)
        fav = Novel.objects.create(name="first favor", desc="Desc", max_chapter=3)
        nuser.favors.add(fav)

    def test_get_and_post(self):
        # TODO: more tests 
        # current only test status code.
        factory = APIRequestFactory()
        request = factory.get('/user/')
        response = NUserViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 200)
        
