
from django.db import models


class Novel(models.Model):
    name = models.CharField(max_length=64)   # in bytes
    # description:
    desc = models.CharField(max_length=256)  # in bytes
    # the last chapter's order
    max_chapter = models.PositiveSmallIntegerField()


class Chapter(models.Model):
    novel = models.ForeignKey(Novel,
              related_name="chapters",  # used to be refered to in `Novel`
              on_delete=models.CASCADE,
            )
    content = models.TextField()  # var-length
