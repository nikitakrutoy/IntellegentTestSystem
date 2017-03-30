# -*- coding: utf8 -*-

from django.conf.urls import url

from .views import reply

urlpatterns = [
    url(r'^bot/(?P<bot_token>.+)/$', reply, name='message'),
]
