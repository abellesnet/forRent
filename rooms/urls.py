# -*- coding: utf-8 -*-
from django.conf.urls import url

from rooms.views import MyRoomsListView, RoomCreateView, RoomDetailView, RoomUpdateView, RoomDeleteView

urlpatterns = [

    url(r'myrooms/$', MyRoomsListView.as_view(), name='myrooms_list'),
    url(r'c/$', RoomCreateView.as_view(), name='room_create'),
    url(r'r/(?P<pk>[0-9]+)/$', RoomDetailView.as_view(), name='room_detail'),
    url(r'u/(?P<pk>[0-9]+)/$', RoomUpdateView.as_view(), name='room_update'),
    url(r'd/(?P<pk>[0-9]+)/$', RoomDeleteView.as_view(), name='room_delete'),

]
