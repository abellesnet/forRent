# -*- coding: utf-8 -*-
from django.conf.urls import url

from rooms.views import RoomCreateView, MyRoomsListView, MyRoomsDetailView

urlpatterns = [

    url(r'create/$', RoomCreateView.as_view(), name='room_create'),
    url(r'myrooms/$', MyRoomsListView.as_view(), name='myrooms_list'),
    url(r'myrooms/(?P<pk>[0-9]+)/$', MyRoomsDetailView.as_view(), name='myrooms_detail'),

]
