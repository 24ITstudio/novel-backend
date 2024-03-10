
from django.db import models


class Novel(models.Model):
    name = models.CharField(max_length=70)   # in bytes
    # description:
    desc = models.CharField(max_length=200)  # in bytes


class Chapter(models.Model):
    novel = models.ForeignKey("Chapter",
              related_name="chapters",  # used to be refered to in `Novel`
              on_delete=models.CASCADE,
            )
    content = models.TextField()  # var-length
