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


import os
import sys
from configparser import ConfigParser as Conf, NoSectionError, NoOptionError
import subprocess
import tkinter as TK
import tkinter.ttk as TTK
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox

from esptool_gui.constants import *
from esptool_gui.settings import *




SLOT = lambda f, *x, **k: lambda: f(*x, **k)


class MainWindow:
    def __init__(self, parent):
        self.parent = parent

        # ***************************************************************
        # combo frame
        comboframe = TK.Frame(self.parent)
        comboframe.grid(row=0, column=0, pady=10, sticky=TK.NW)

        comboframe.columnconfigure(1, weight=1)

        self.conf_combo_var = TK.StringVar()

        conf_label = TK.Label(comboframe, text="Configuration:")
        self.conf_combo = TTK.Combobox(comboframe, width=50,
                                       textvariable=self.conf_combo_var,)
        conf_btn_add = TK.Button(comboframe, text="Add",
                            command=lambda: self.__add_config(self.conf_combo.get()))
        conf_btn_del = TK.Button(comboframe, text="Del",
                            command=lambda: self.__del_config(self.conf_combo.get()))

        conf_label.grid(row=0, column=0, padx=2, pady=2, sticky=TK.W)
        self.conf_combo.grid(row=0, column=1, padx=2, pady=2, sticky=TK.EW)
        conf_btn_add.grid(row=0, column=3, padx=2, pady=2)
        conf_btn_del.grid(row=0, column=4, padx=2, pady=2)

        # ***************************************************************
        # top frame
        topframe = TK.Frame(self.parent)
        topframe.grid(row=1, column=0, sticky=TK.NSEW)

        topframe.columnconfigure(1, weight=1)

        self.files = {}
        for i in range(n_file_entries):
            var_use_flag = TK.BooleanVar()
            var_path = TK.StringVar()
            var_offset = TK.StringVar()

            file_chbx = TK.Checkbutton(topframe, variable=var_use_flag,
                                       command=SLOT(self.update_file_entry, i))
            file_path = TK.Label(topframe, relief=TK.SUNKEN,
                                 textvariable=var_path, activebackground='white',
                                 anchor=TK.W, state=TK.DISABLED)
            file_btn = TK.Button(topframe, text="...",
                                 command=SLOT(self.get_file_name, i),
                                 state=TK.DISABLED)
            file_offset_label = TK.Label(topframe, text="Offset:",
                                         state=TK.DISABLED)
            file_offset = TK.Entry(topframe, width=12, textvariable=var_offset,
                                   state=TK.DISABLED)

            file_chbx.grid(row=i, column=0, padx=2, pady=2)
            file_path.grid(row=i, column=1, padx=2, pady=2, sticky=TK.EW)
            file_btn.grid(row=i, column=2, padx=2, pady=1)
            file_offset_label.grid(row=i, column=3, padx=2, pady=2)
            file_offset.grid(row=i, column=4, padx=2, pady=2)

            self.files[i] = ({key_v_part_use_flag: var_use_flag,
                              key_v_part_path: var_path,
                              key_v_part_offset: var_offset,
                              key_w_path: file_path,
                              key_w_btn: file_btn,
                              key_w_offset_lbl: file_offset_label,
                              key_w_offset: file_offset})

        # config
        self.sfname = 'espsettings.ini'
        if not os.path.exists(self.sfname):
            with open(self.sfname, mode='w+'): pass

        self.conf = Conf()
        self.conf.read(self.sfname)
        self.__read_settings()

        # ***************************************************************
        # bottom frame
        botframe = TK.Frame(self.parent)
        botframe.grid(row=2, column=0, sticky=TK.NSEW)

        botframe.columnconfigure(0, weight=1)
        botframe.rowconfigure(1, weight=1)

        # shell and scroll
        shell_label = TK.Label(botframe, text="Shell log:", anchor=TK.NW)
        self.shell = TK.Text(botframe, height=20)
        self.scrollbar = TK.Scrollbar(botframe, orient=TK.VERTICAL,
                                           command=self.shell.yview)
        self.shell.configure(yscrollcommand=self.scrollbar.set)

        shell_label.grid(row=0, column=0, padx=2, pady=2, sticky=TK.W)
        self.shell.grid(row=1, column=0, sticky=TK.NSEW)
        self.scrollbar.grid(row=1, column=1, sticky=TK.NS)

        # status bar
        self.statusbar = TK.Label(botframe, text="Ready...", anchor=TK.W)
        self.statusbar.after(5000, self.clear_status_bar)
        self.statusbar.grid(row=2, column=0, sticky=TK.EW)

        # ***************************************************************
        # main window
        window = self.parent.winfo_toplevel()
        window.columnconfigure(0, weight=1)
        window.rowconfigure(2, weight=1)

        self.parent.geometry("{0}x{1}+{2}+{3}".format(640, 780, 150, 150))
        self.parent.title("esptool.py GUI")
        self.parent.bind("<Control-q>", self.app_quit)

    def set_status_bar(self, text, timeout=5000):
        self.statusbar["text"] = text
        if timeout:
            self.statusbar.after(timeout, self.clear_status_bar)

    def clear_status_bar(self):
        self.statusbar["text"] = ""

    def get_file_name(self, key):
        if not self.okay_to_continue():
            return

        current_sec = self.conf_option_get(key_conf_sec_general, key_conf_current_set_name)
        init_dir = self.conf_option_get(current_sec, key_conf_last_dir)

        filename = filedialog.askopenfilename(
            title="Choose firmware part",
            initialdir=init_dir,
            filetypes=[("Binary files", "*.bin")],
            defaultextension=".bin", parent=self.parent)
        if filename:
            # remember the last used directory
            if 'current_sec' not in locals():
                current_sec = key_conf_sec_current
            self.conf_option_set(current_sec, key_conf_last_dir, os.path.dirname(filename))

            fe = self.files[key]
            fe[key_v_part_path].set(filename)
            self.__reset_offset(fe[key_v_part_offset])

    def update_file_entry(self, key):
        fe_used = self.files[key][key_v_part_use_flag].get()
        self.__update_fe(self.files[key], fe_used)

    def app_quit(self, event=None):
        self.__save_settings()
        if self.okay_to_continue():
            self.parent.destroy()

    def okay_to_continue(self):
        # if not self.dirty:
        #     return True
        # reply = messagebox.askyesnocancel(
        #                 "Bookmarks - Unsaved Changes",
        #                 "Save unsaved changes?", parent=self.parent)
        # if reply is None:
        #     return False
        # if reply:
        #     return self.fileSave()
        return True

    def __update_fe(self, entry, enabled):
        entry[key_w_btn].config(state=TK.ACTIVE if enabled else TK.DISABLED)
        entry[key_w_path].config(state=TK.ACTIVE if enabled else TK.DISABLED)
        entry[key_w_offset_lbl].config(state=TK.ACTIVE if enabled else TK.DISABLED)
        entry[key_w_offset].config(state=TK.NORMAL if enabled else TK.DISABLED)

    def __reset_offset(self, var_offset):
        var_offset.set('0x')

    def __combo_config_name_set(self, name):
        self.conf_combo_var.set(name)

    def __combo_config_name_set_current(self):
        curr = self.conf_option_get(key_conf_sec_general, key_conf_current_set_name)
        self.__combo_config_name_set(curr[len(key_conf_prefix):] if curr else
                                key_conf_sec_default[len(key_conf_prefix):])

    def __combo_config_name_get(self):
        return ''.join([key_conf_prefix, self.conf_combo_var.get()])

    def __save_settings(self):
        curr = self.__combo_config_name_get()
        self.conf_option_set(key_conf_sec_general, key_conf_current_set_name, curr)

        sec = self.conf_option_get(key_conf_sec_general, key_conf_current_set_name)
        for k, fe in self.files.items():
            mkopt = lambda opt: '.'.join((str(k), opt))
            self.conf_option_set(sec, mkopt(key_v_part_path), fe[key_v_part_path].get())
            self.conf_option_set(sec, mkopt(key_v_part_offset), fe[key_v_part_offset].get())
            self.conf_option_set(sec, mkopt(key_v_part_use_flag), str(bool(fe[key_v_part_use_flag].get())))

        with open(self.sfname, 'w') as f:
            self.conf.write(f)

    def __read_settings(self):
        for sec in self.conf.sections():
            for opt in self.conf.options(sec):
                keys = opt.split('.')
                if len(keys) == 2:
                    key_fe, optname = int(keys[0]), keys[1]
                    if optname != key_v_part_use_flag:
                        val = self.conf_option_get(sec, opt, str)
                    else:
                        val = self.conf_option_get(sec, opt, bool)
                    self.files[key_fe][optname].set(val)

        # fill combo with configurations list
        self.conf_combo['values'] = [conf[len(key_conf_prefix):]
                                      for conf in self.conf.sections()
                                        if conf.startswith(key_conf_prefix)]
        self.__combo_config_name_set_current()

    def __add_config(self, config_name):
        print("add:", config_name)

    def __del_config(self, config_name):
        print("remove:", config_name)

    def conf_option_set(self, section, option, value):
        c = self.conf
        if not c.has_section(section):
            c.add_section(section)
        c.set(section, option, str(value))

    def conf_option_get(self, section, option, type=str):
        c = self.conf
        if not c.has_section(section):
            c.add_section(section)

        val = ""
        if not c.has_option(section, option):
            return val

        if type is str:
            val = c.get(section, option, raw=True)
        elif type is bool:
            val = c.getboolean(section, option, raw=True)
        elif type is int:
            val = c.getint(section, option, raw=True)
        else:
            val = c.getfloat(section, option, raw=True)

        return val


if __name__ == '__main__':
    application = TK.Tk()
    path = os.path.join(os.path.dirname(__file__), "rc/")
    if sys.platform.startswith("win"):
        icon = path + "app_icon.ico"
        application.iconbitmap(icon, default=icon)
    else:
        img = TK.PhotoImage(file=path + 'app_icon.png')
        application.tk.call('wm', 'iconphoto', application._w, img)
    window = MainWindow(application)
    application.minsize(500, 650)
    application.protocol("WM_DELETE_WINDOW", window.app_quit)
    application.mainloop()
