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
    path = os.path.join(os.path.dirname(__file__), "rc/")
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
