# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from rest_framework.viewsets import ReadOnlyModelViewSet

from users.serializers import UserSerializer


class UserViewSet(ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
