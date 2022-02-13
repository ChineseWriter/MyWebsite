#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :urls.py
# @Time      :2022/2/13 16:31
# @Author    :Amundsen Severus Rubeus Bjaaland


from django.urls import path

from . import views


urlpatterns = [
    path('', views.home.index, name='index'),
]
