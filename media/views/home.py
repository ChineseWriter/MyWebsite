#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :home.py
# @Time      :2022/2/11 17:25
# @Author    :Amundsen Severus Rubeus Bjaaland


from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello!")
