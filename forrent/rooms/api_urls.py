# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from rooms.api_views import RoomBookingViewSet

router = DefaultRouter()
router.register(r'roombooking', RoomBookingViewSet, base_name='roombooking')

urlpatterns = [
    url(r'^1.0/', include(router.urls)),
]
