# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer

from users.models import Profile


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'date_joined',)


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        exclude = ('created_at', 'modified_at',)
