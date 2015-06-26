#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""About window
"""

__author__ = 'remico <remicollab+github@gmal.com>'

import os.path
import tkinter as TK
from .constants import *


def show_about(parent):
    """
    Create an 'About' window
    :param parent: the parent widget for the About window
    :return: None
    """
    top = TK.Toplevel(parent)
    top.resizable(width=TK.FALSE, height=TK.FALSE)
    top.wm_title("About")
    top.bind("<Escape>", lambda *x: top.destroy())

    text_ = "{name}\n" \
            "{ver}\n\n" \
            "GUI wrapper for ESP8266 ROM Bootloader esptool.py\n" \
            "Based on python3 and Tkinter\n\n" \
            "{developer}\n" \
            "{url}" \
            .format(name=app_name, ver=app_version, developer=app_developer, url=app_url)

    icon_path = os.path.join(os.path.dirname(__file__), "rc/app_icon.png")
    icon = TK.PhotoImage(file=icon_path)

    icon_lbl = TK.Label(top, image=icon, text=text_, compound=TK.TOP)
    icon_lbl.image = icon

    ok_btn = TK.Button(top, text="OK", width=10, command=top.destroy)
    ok_btn.focus_set()

    icon_lbl.grid(row=0, padx=20, pady=20, sticky=TK.NW)
    ok_btn.grid(row=1, padx=20, pady=20)
