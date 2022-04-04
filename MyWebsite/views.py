# coding = UTF-8


import importlib

from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse


TOOL_LIST = ("media", "company", "ChatRecord")


def index(request):
    return render(request, "MyWebsite/index.html")


def jump_to_tool(request, tool_name: str):
    if tool_name not in TOOL_LIST:
        return HttpResponse()
    application = importlib.import_module(tool_name)
    return render(
        request, "MyWebsite/tool_preview.html",
        {
            "app_name": application.APPNAME,
            "app_verbose_name": application.APPVERBOSENAME,
            "app_desc": application.DESCRIPTION,
            "app_url": reverse(f"{application.APPNAME}:index")
        }
    )
