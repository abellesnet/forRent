# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.contrib.auth.views import login, logout

from users.views import CreateUserView, ProfileDetailView, ProfileUpdateView

urlpatterns = [

    url(r'user/$', CreateUserView.as_view(), name='user_create'),
    url(r'login/$', login, {'template_name': 'login_form.html'}, name='login'),
    url(r'logout/$', logout, {'next_page': '/'}, name='logout'),

    url(r'r/(?P<pk>[0-9]+)/$', ProfileDetailView.as_view(), name='profile_detail'),
    url(r'u/(?P<pk>[0-9]+)/$', ProfileUpdateView.as_view(), name='profile_update'),

]
