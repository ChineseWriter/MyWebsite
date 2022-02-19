#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :home.py
# @Time      :2022/2/11 17:25
# @Author    :Amundsen Severus Rubeus Bjaaland


from django.shortcuts import render
from django.views.decorators.http import require_GET

from .. import forms


@require_GET
def index(request):
    return render(request, "media/index.html", {"MusicSelectForm": forms.home.MusicSelectForm()})
