# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from users.api_views import UserViewSet, ProfileViewSet

router = DefaultRouter()
router.register(r'user', UserViewSet, base_name='user')
router.register(r'profile', ProfileViewSet, base_name='profile')

urlpatterns = [
    url(r'^1.0/', include(router.urls)),
]
