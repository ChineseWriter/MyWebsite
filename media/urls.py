#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :urls.py
# @Time      :2022/2/11 17:24
# @Author    :Amundsen Severus Rubeus Bjaaland


from django.urls import path

from . import views


app_name = "media"
urlpatterns = [
    path('', views.home.index, name='index'),
    path('music/select', views.music.select_music, name='music-select'),
    path('music/detail', views.music.music_detail, name='music-detail'),
    path('music/download', views.music.download_music, name='music-download'),
]
