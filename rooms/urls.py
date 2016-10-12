# -*- coding: utf-8 -*-
from django.conf.urls import url

from rooms.views import CreateRoomView

urlpatterns = [

    url(r'$', CreateRoomView.as_view(), name='room_create'),

]
