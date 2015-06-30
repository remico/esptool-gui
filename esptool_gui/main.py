#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
"""

__author__ = 'remico <remicollab+github@gmail.com>'

import os, sys
import tkinter as TK
from .mainwindow import MainWindow
from .settings import INISettings
from .executor import Executor


def main():
    application = TK.Tk()

    # check if the application is frozen
    if getattr(sys, 'frozen', False):
        datadir = os.path.dirname(sys.executable)
    else:
        datadir = os.path.dirname(__file__)

    path = os.path.join(datadir, "rc/")
    if sys.platform.startswith("win"):
        icon = path + "app_icon.ico"
        application.iconbitmap(icon, default=icon)
    else:
        img = TK.PhotoImage(file=path + 'app_icon.png')
        application.tk.call('wm', 'iconphoto', application._w, img)
    window = MainWindow(application, INISettings(), Executor(application))
    application.minsize(650, 500)
    application.protocol("WM_DELETE_WINDOW", window.app_quit)
    application.mainloop()
