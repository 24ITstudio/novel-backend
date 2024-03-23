
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import Novel,Chapter


class NovelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Novel
        fields = "__all__"


class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = "__all__"
        extra_kwargs = dict(
           content=dict(write_only=True),
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Chapter.objects.all(),
                fields=['novel', 'chapter_ord'],
                message="this chapter of given novel has alreadly exists"
            )
        ]
    
    def validate_chapter_ord(self, c_ord):
        if not c_ord > 0:
            raise serializers.ValidationError("chapter_ord must be a positive integer")
        return c_ord
    def validate(self, attrs):
        novel: Novel = attrs['novel']
        c_ord = attrs['chapter_ord']
        if c_ord > novel.max_chapter:
            raise serializers.ValidationError("the chapter order given exceeds novel's max_chapter")
        return super().validate(attrs)