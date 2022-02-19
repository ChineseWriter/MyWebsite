# coding = UTF-8


import os
import sys


TOOL_PATH = os.path.abspath("./media/Tools")

if TOOL_PATH not in sys.path:
    sys.path.append(TOOL_PATH)
