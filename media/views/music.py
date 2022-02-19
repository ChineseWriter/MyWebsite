#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :music.py
# @Time      :2022/2/14 9:56
# @Author    :Amundsen Severus Rubeus Bjaaland


import os

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST, require_GET
from django.urls import reverse
from django.core.files import File

from .. import forms
from ..models import Poster, Singer, Music

from MediaDL.Engines import MediaController
from MediaDL.Objects import Music as MusicObject


MEDIA_CONTROLLER = MediaController()
SUPPORT_WEBSITE = {"KuGou": "KG", "WangYiYun": "WYY", "QQMusic": "QM"}


try:
    os.mkdir("./buffer")
except FileExistsError:
    pass


@require_POST
def select_music(request):
    music_select_form = forms.home.MusicSelectForm(request.POST)
    if music_select_form.is_valid():
        music_select_result = MEDIA_CONTROLLER.select_music(music_select_form.data["music_name"])
        params = {
            "select_keyword": music_select_form.data["music_name"],
            "music_select_result": music_select_result
        }
        return render(request, "media/music/select_result.html", params)
    return HttpResponseRedirect(reverse("media:index"))


@require_GET
def music_detail(request):
    params = request.GET
    one_music = MusicObject(master_id=params.get("master_id"), sub_id=params.get("sub_id"))
    one_music = MEDIA_CONTROLLER.get_music_info(one_music)
    music_select_result = Music.objects.filter(
        source_site=SUPPORT_WEBSITE[one_music.source_site],
        master_id=one_music.master_id,
        sub_id=one_music.sub_id
    )
    if not music_select_result.exists():
        singer_buffer = []
        for one_singer in one_music.singer_list.self_objects:
            obj, created = Singer.objects.get_or_create(
                name=one_singer.name,
                source_site=SUPPORT_WEBSITE[one_singer.source_site],
                master_id=one_singer.id,
                description=one_singer.description
            )
            singer_buffer.append(obj)
        poster_buffer = []
        for i in one_music.poster_list.self_objects:
            poster_select_result = Poster.objects.filter(self_source=i.self_source)
            if not poster_select_result.exists():
                with open("./buffer/poster_buffer", "wb+") as poster_file:
                    poster_file.write(i.self_object)
                    poster_file.seek(0)
                    poster_object = Poster.objects.create(
                        source_site=i.source_site,
                        self_source=i.self_source,
                        self_object=File(poster_file, one_music.master_id + ".jpg")
                    )
                try:
                    os.remove("./buffer/poster_buffer")
                except (FileNotFoundError, OSError):
                    pass
            else:
                poster_object = poster_select_result.first()
            poster_buffer.append(poster_object)
        one_music.save("./buffer", lyric_file=False)
        with open(f"./buffer/{one_music.singer_list.name_list} - {one_music.name}.mp3", "rb") as music_file:
            music_object: Music = Music.objects.create(
                name=one_music.name,
                source_site=SUPPORT_WEBSITE[one_music.source_site],
                self_source=one_music.self_source,
                self_object=File(music_file, one_music.master_id+".mp3"),
                lyrics=one_music.lyrics,
                album=one_music.album,
                master_id=one_music.master_id,
                sub_id=one_music.sub_id
            )
        for i in singer_buffer:
            music_object.singers.add(i)
        for i in poster_buffer:
            music_object.posters.add(i)
        music_object.save()
        try:
            os.remove(f"./buffer/{one_music.singer_list.name_list} - {one_music.name}.mp3")
        except (FileNotFoundError, OSError):
            pass
    else:
        music_object = music_select_result.first()
    params = {"music_object": music_object, "one_music": one_music}
    return render(request, "media/music/music_detail.html", params)

