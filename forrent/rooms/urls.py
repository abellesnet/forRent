# -*- coding: utf-8 -*-
from django.conf.urls import url, include

from rooms import api_urls
from rooms.views import MyRoomsListView, RoomCreateView, RoomDetailView, RoomUpdateView, RoomDeleteView, RoomListView, \
    RoomBookingListView, RoomBookingDeleteView

urlpatterns = [

    url(r'^api/', include(api_urls)),

    url(r'^myrooms/$', MyRoomsListView.as_view(), name='myrooms_list'),
    url(r'^c/$', RoomCreateView.as_view(), name='room_create'),
    url(r'^r/(?P<pk>[0-9]+)/$', RoomDetailView.as_view(), name='room_detail'),
    url(r'^u/(?P<pk>[0-9]+)/$', RoomUpdateView.as_view(), name='room_update'),
    url(r'^d/(?P<pk>[0-9]+)/$', RoomDeleteView.as_view(), name='room_delete'),
    url(r'^$', RoomListView.as_view(), name='room_list'),

    url(r'^booking/$', RoomBookingListView.as_view(), name='roombooking_list'),
    url(r'^booking/d/(?P<pk>[0-9]+)/$', RoomBookingDeleteView.as_view(), name='roombooking_delete'),

]
