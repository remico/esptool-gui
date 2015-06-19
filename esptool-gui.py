#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version. It is provided for educational
# purposes and is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.

"""Simple GUI wrapper for esptool.py (https://github.com/themadinventor/esptool)
based on python3 and Tkinter
"""

__author__ = 'remico <remicollab+github@gmal.com>'

import os, sys
import tkinter as TK
from esptool_gui.mainwindow import MainWindow
from esptool_gui.settings import INISettings
from esptool_gui.executor import Executor


if __name__ == '__main__':
    application = TK.Tk()
    path = os.path.join(os.path.dirname(__file__), "esptool_gui/rc/")
    if sys.platform.startswith("win"):
        icon = path + "app_icon.ico"
        application.iconbitmap(icon, default=icon)
    else:
        img = TK.PhotoImage(file=path + 'app_icon.png')
        application.tk.call('wm', 'iconphoto', application._w, img)
    window = MainWindow(application, INISettings(), Executor(application))
    application.minsize(650, 650)
    application.protocol("WM_DELETE_WINDOW", window.app_quit)
    application.mainloop()
