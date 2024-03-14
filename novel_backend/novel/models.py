
from django.db import models


# 0 to at least 32767
_ChapterOrderType = models.PositiveSmallIntegerField

class Novel(models.Model):
    name = models.CharField(max_length=64)   # in bytes
    # description:
    desc = models.CharField(max_length=256)  # in bytes
    # the last chapter's order
    max_chapter = _ChapterOrderType()

    tag = models.CharField(max_length=16, default="")


class Chapter(models.Model):
    novel = models.ForeignKey(Novel,
              related_name="chapters",  # used to be referred to in `Novel`
              on_delete=models.CASCADE,
            )
    chapter_ord = _ChapterOrderType()
    content = models.TextField()  # var-length
