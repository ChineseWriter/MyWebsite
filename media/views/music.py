#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :music.py
# @Time      :2022/2/14 9:56
# @Author    :Amundsen Severus Rubeus Bjaaland


import os
from io import BytesIO
from zipfile import ZipFile
from urllib.parse import quote

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


def _download_and_save_music(params):
	one_music = MusicObject(master_id=params.get("master_id"), sub_id=params.get("sub_id"), source_site=params.get(
		"source_site"))
	one_music = MEDIA_CONTROLLER.get_music_info(one_music)
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
			self_object=File(music_file, one_music.master_id + ".mp3"),
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
	return music_object


@require_GET
def music_detail(request):
	params = request.GET
	music_select_result = Music.objects.filter(
		master_id=params.get("master_id"),
		sub_id=params.get("sub_id")
	)
	if music_select_result.exists():
		music_object = music_select_result.first()
	else:
		music_object = _download_and_save_music(params)
	params = {
		"music_object": music_object,
		"singers": music_object.singers.all(),
		"singers_name": "、".join([one_singer.name for one_singer in music_object.singers.all()]),
		"music_source_site": music_object.get_source_site_display()
	}
	posters = music_object.posters.all()
	if posters:
		params["poster_url"] = music_object.posters.all()[0].self_object.url
	else:
		params["poster_url"] = "https://www.kugou.com/common/images/logo4openmusicplan.gif"
	return render(request, "media/music/music_detail.html", params)

@require_GET
def download_music(request):
	music_id = request.GET.get("id")
	music_object = Music.objects.filter(id=music_id).first()
	music_zip_file = BytesIO()
	music_singers_name = "、".join([one_singer.name for one_singer in music_object.singers.all()])
	music_file_path = music_object.self_object.path
	with open(music_file_path, "rb") as music_file:
		music_content = music_file.read()
	with ZipFile(music_zip_file, 'w') as zip_file:
		zip_file.writestr(f"{music_singers_name} - {music_object.name}.mp3", music_content)
		zip_file.writestr(f"{music_singers_name} - {music_object.name}.lrc", music_object.lyrics)
	response = HttpResponse(music_zip_file.getvalue(), content_type='application/x-zip-compressed')
	response['Content-Disposition'] = f'attachment; filename={quote(music_singers_name)} - {quote(music_object.name)}.zip'
	return response
