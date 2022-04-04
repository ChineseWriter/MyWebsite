# coding = UTF-8


import os
import sys


TOOL_PATH = os.path.abspath("./media/Tools")
APPNAME = "media"
APPVERBOSENAME = "媒体文件下载器"
DESCRIPTION = "主要用于从各大网站上下载指定的媒体文件，包括小说、图片、音乐、视频等"

if TOOL_PATH not in sys.path:
    sys.path.append(TOOL_PATH)
