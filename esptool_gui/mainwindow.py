#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
"""

__author__ = 'remico <remicollab+github@gmal.com>'

import os
import tkinter as TK
import tkinter.ttk as TTK
import tkinter.filedialog as filedialog
# import tkinter.messagebox as messagebox
from .constants import *


SLOT = lambda f, *x, **k: lambda: f(*x, **k)


class MainWindow:
    def __init__(self, parent, settings, executor):
        self.parent = parent
        self.S = settings
        self.executor = executor

        # ***************************************************************
        # combo frame
        comboframe = TK.Frame(self.parent)
        comboframe.grid(row=0, column=0, pady=10, sticky=TK.NW)

        comboframe.columnconfigure(1, weight=1)

        self.conf_combo_var = TK.StringVar()
        self.conf_combo_var.trace('w', self.__combo_clicked)

        conf_label = TK.Label(comboframe, text="Configuration:")
        self.conf_combo = TTK.Combobox(comboframe, width=50,
                                       textvariable=self.conf_combo_var)
        conf_btn_add = TK.Button(comboframe, text="Save",
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
                                       command=SLOT(self.update_file_entry_state, i))
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
                              key_w_use_flag: file_chbx,
                              key_w_path: file_path,
                              key_w_btn: file_btn,
                              key_w_offset_lbl: file_offset_label,
                              key_w_offset: file_offset})

            self.__reset_offset(var_offset)

        # ***************************************************************
        # middle frame
        midframe = TK.Frame(self.parent)
        midframe.grid(row=2, column=0, sticky=TK.NSEW)

        midframe.columnconfigure(0, weight=1)

        flash_btn = TK.Button(midframe, text="Flash", command=self.__execute)
        flash_btn.grid(row=0, column=0, padx=10, pady=10, sticky=TK.E)

        # ***************************************************************
        # bottom frame
        botframe = TK.Frame(self.parent)
        botframe.grid(row=3, column=0, sticky=TK.NSEW)

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
        window.rowconfigure(3, weight=1)

        self.parent.geometry("{0}x{1}+{2}+{3}".format(640, 780, 350, 150))
        self.parent.title("esptool GUI")
        self.parent.bind("<Control-q>", self.app_quit)

        self.__read_settings()

    def set_status_bar(self, text, timeout=5000):
        self.statusbar["text"] = text
        if timeout:
            self.statusbar.after(timeout, self.clear_status_bar)

    def clear_status_bar(self):
        self.statusbar["text"] = ""

    def get_file_name(self, key):
        current_conf = self.__combo_config_name_get()
        init_dir = self.S.last_used_path(current_conf)

        filename = filedialog.askopenfilename(
            title="Choose firmware part",
            initialdir=init_dir if init_dir else '.',
            filetypes=[("Binary files", "*.bin")],
            defaultextension=".bin", parent=self.parent)

        if filename:
            # remember the last used directory
            self.S.save_last_used_path(current_conf, os.path.dirname(filename))

            fe = self.files[key]
            fe[key_v_part_path].set(filename)
            self.__reset_offset(fe[key_v_part_offset])

    def update_file_entry_state(self, key):
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

    def __combo_config_name_get(self):
        return self.conf_combo_var.get()

    def __save_settings(self):
        curr = self.__combo_config_name_get()
        self.S.save_current_configuration(curr)
        self.S.save_conf_file_entries(curr, self.files)
        self.S.write()

    def __read_settings(self):
        # fill file entries
        self.__fill_fes()

        # fill combo with configurations list
        self.conf_combo['values'] = self.S.configurations()
        current_configuration = self.S.current_configuration()
        self.__combo_config_name_set(current_configuration)

    def __fill_fes(self, conf=None):
        for key_fe, fe in self.S.conf_file_entries(conf).items():
             for key_opt, val in fe.items():
                 self.files[key_fe][key_opt].set(val)

                 if key_opt == key_v_part_use_flag:
                     self.update_file_entry_state(key_fe)


    def __add_config(self, config_name):
        self.__save_settings()
        l = list(self.conf_combo['values'])
        if config_name in l:
            return
        l.append(config_name)
        self.conf_combo['values'] = l

    def __del_config(self, config_name):
        l = list(self.conf_combo['values'])
        if len(l) == 1:
            return
        l.remove(config_name)
        self.conf_combo['values'] = l
        self.conf_combo.current(0)
        self.S.remove(config_name)
        self.__save_settings()

    def __combo_clicked(self, *a):
        self.__fill_fes(self.__combo_config_name_get())

    def __execute(self):
        parts = [(fe[key_v_part_offset].get(), fe[key_v_part_path].get())
                    for fe in self.files.values()
                        if fe[key_v_part_use_flag].get()]
        print(parts)
        self.executor.run(parts, out=self.shell)
