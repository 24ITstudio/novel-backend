from django.db import models
from django.contrib.auth.models import User
from novel.models import Novel


class NUser(User):
    auth_token = models.CharField(max_length=64)
    favors = models.ManyToManyField(Novel)
    # ref https://docs.djangoproject.com/zh-hans/4.2/topics/db/examples/many_to_many/
