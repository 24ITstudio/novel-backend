"""novel_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from novel.views import NovelViewSet, HotNovelViewSet,ChaptersViewSet

from user.views import NUserViewSet, CreateNUserSet, FavorNUserSet, username




urlpatterns = [
    path("admin/", admin.site.urls),
]

urlpatterns.append(
    path('token-auth/', views.obtain_auth_token)
)
# ref https://blog.csdn.net/qq_39980136/article/details/89503850
#     https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication

router = DefaultRouter()
router.register('novel', NovelViewSet)
router.register('hotnovel', HotNovelViewSet,basename='hotnovel')
router.register('user', NUserViewSet)
router.register('register', CreateNUserSet,basename='register')
router.register('chapter', ChaptersViewSet)

urlpatterns.append(
    path('', include(router.urls)),
)

urlpatterns.append(
  path('favor/<int:pk>/', FavorNUserSet.as_view())
)

urlpatterns.append(
  path('user-id/<str:username>/', username)
)
