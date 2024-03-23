
from django.contrib.auth.hashers import make_password
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
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
    def update(self, instance, validated_data):
        raw_passwd = validated_data.get('password', None)
        if raw_passwd is not None:
            validated_data['password'] = make_password(raw_passwd)
        return super().update(instance, validated_data)
        
