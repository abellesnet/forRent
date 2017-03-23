# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from rooms.api_views import RoomBookingViewSet, RoomRatingViewSet, RoomCommentViewSet, RoomViewSet

router = DefaultRouter()
router.register(r'roombooking', RoomBookingViewSet, base_name='roombooking')
router.register(r'roomrating', RoomRatingViewSet, base_name='roomrating')
router.register(r'roomcomment', RoomCommentViewSet, base_name='roomcomment')
router.register(r'room', RoomViewSet, base_name='room')

urlpatterns = [
    url(r'^1.0/', include(router.urls)),
]
