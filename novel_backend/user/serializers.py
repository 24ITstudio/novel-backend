
from rest_framework import serializers
from .models import NUser


class NUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NUser
        fields = "__all__"
        extra_kwargs = dict(
            # make password not transmitted and shown when getting info
            password=dict(write_only=True),
            favors=dict(allow_empty=True, required=False),
        )
