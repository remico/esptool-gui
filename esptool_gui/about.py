#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""About window
"""

__author__ = 'remico <remicollab+github@gmail.com>'

import os.path
import tkinter as TK
from .constants import *


def wnd_about(parent):
    """
    Create an 'About' window
    :param parent: the parent widget for the About window
    :return: None
    """
    def close(*ignore):
        parent.focus_set()
        top.destroy()

    top = TK.Toplevel(parent)
    top.transient(parent)
    top.resizable(width=TK.FALSE, height=TK.FALSE)
    top.title("About")
    top.bind("<Escape>", close)

    text_ = "{app_name}\n" \
            "{app_ver}\n\n" \
            "GUI wrapper for ESP8266 ROM Bootloader esptool.py\n" \
            "Based on python3 and Tkinter\n\n" \
            "{dev_name} <{dev_email}>\n" \
            "{app_url}" \
            .format(app_name=app_name,
                    app_ver=app_version,
                    dev_name=app_developer,
                    dev_email=app_developer_email,
                    app_url=app_url)

    icon_path = os.path.join(os.path.dirname(__file__), "rc/app_icon.png")
    icon = TK.PhotoImage(file=icon_path)

    icon_lbl = TK.Label(top, image=icon, text=text_, compound=TK.TOP)
    icon_lbl.image = icon

    ok_btn = TK.Button(top, text="OK", width=10, command=top.destroy)
    ok_btn.focus_set()

    icon_lbl.grid(row=0, padx=20, pady=20, sticky=TK.NW)
    ok_btn.grid(row=1, padx=20, pady=20)
