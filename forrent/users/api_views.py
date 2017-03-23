# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from rest_framework.viewsets import ReadOnlyModelViewSet

from users.models import Profile
from users.serializers import UserSerializer, ProfileSerializer


class UserViewSet(ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProfileViewSet(ReadOnlyModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
