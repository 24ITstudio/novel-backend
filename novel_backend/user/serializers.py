
from rest_framework import serializers
from .models import NUser


class NUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NUser
        fields = "__all__"
        extra_kwargs = dict(
            favors = dict(allow_empty=True),
        )
