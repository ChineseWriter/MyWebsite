#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :home.py
# @Time      :2022/2/11 17:25
# @Author    :Amundsen Severus Rubeus Bjaaland


from django.shortcuts import render
from django.views.decorators.http import require_GET

from .. import forms


APPNAME = "media"
APPVERBOSENAME = "媒体文件下载器"
DESCRIPTION = "主要用于从各大网站上下载指定的媒体文件，包括小说、图片、音乐、视频等"


@require_GET
def index(request):
    return render(
        request, "media/index.html",
        {
            "MusicSelectForm": forms.home.MusicSelectForm(),
            "AppName": APPNAME,
            "AppVerboseName": APPVERBOSENAME,
            "AppDesc": DESCRIPTION
        }
    )
