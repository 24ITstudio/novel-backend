from django.test import TestCase
# ref https://docs.djangoproject.com/zh-hans/4.2/topics/testing/overview/

from rest_framework.test import APIRequestFactory
from .views import NUserViewSet
from .models import NUser


U1NAME = "user 1 name"


class ApiTestCase(TestCase):
    def setUp(self):
        NUser.objects.create(username=U1NAME)

    def test_user(self):
        # test status code and data
        factory = APIRequestFactory()
        request = factory.get('/user/')
        response = NUserViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data[0]['username'], U1NAME)
