# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.contrib.auth.views import login, logout

from users.views import CreateUserView

urlpatterns = [

    url(r'user/$', CreateUserView.as_view(), name='user_create'),
    url(r'login/$', login, {'template_name': 'login_form.html'}, name='login'),
    url(r'logout/$', logout, {'next_page': '/'}, name='logout'),

]
