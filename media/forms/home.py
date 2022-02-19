#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :home.py
# @Time      :2022/2/14 9:47
# @Author    :Amundsen Severus Rubeus Bjaaland


from django import forms


class MusicSelectForm(forms.Form):
    music_name = forms.CharField(label='音乐名称', max_length=20)
