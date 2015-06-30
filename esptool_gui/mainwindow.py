#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Main UI window
"""

__author__ = 'remico <remicollab+github@gmail.com>'

import os
import tkinter as TK
import tkinter.ttk as TTK
import tkinter.filedialog as filedialog
from .constants import *
from .about import wnd_about


SLOT = lambda f, *x, **k: lambda: f(*x, **k)


class MainWindow:
    def __init__(self, parent, settings, executor):
        self.parent = parent
        self.S = settings
        self.executor = executor

        # ***************************************************************
        # frames
        comboframe = self.__init_combo_frame(self.parent)
        topframe = self.__init_top_frame(self.parent)
        midframe = self.__init_mid_frame(self.parent)
        botframe = self.__init_bot_frame(self.parent)

        comboframe.grid(row=0, column=0, pady=10, sticky=TK.NSEW)
        topframe.grid(row=1, column=0, sticky=TK.NSEW)
        midframe.grid(row=2, column=0, pady=10, sticky=TK.NSEW)
        botframe.grid(row=3, column=0, sticky=TK.NSEW)

        # ***************************************************************
        # entire window
        window = self.parent.winfo_toplevel()
        window.columnconfigure(0, weight=1)
        window.rowconfigure(3, weight=1)

        self.parent.geometry("{0}x{1}+{2}+{3}".format(768, 600, 150, 50))
        self.parent.title(" - ".join([app_name, app_version]))
        self.parent.bind("<Control-q>", self.app_quit)

        self.__read_settings()

    def __init_combo_frame(self, parent):
        frame = TK.Frame(parent)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(5, weight=1000)

        self.var_conf_combo = TK.StringVar()
        self.var_conf_combo.trace('w', self.__combo_clicked)

        conf_label = TK.Label(frame, text="Configuration:")
        self.conf_combo = TTK.Combobox(frame, width=50,
                                       textvariable=self.var_conf_combo)
        conf_btn_add = TK.Button(frame, text="Save",
                            command=lambda: self.__add_config(self.conf_combo.get()))
        conf_btn_del = TK.Button(frame, text="Del",
                            command=lambda: self.__del_config(self.conf_combo.get()))
        help_btn = TK.Button(frame, text="Help", command=self.__help)
        about_btn = TK.Button(frame, text="About", command=self.__about)

        conf_label.grid(row=0, column=0, padx=2, pady=2, sticky=TK.W)
        self.conf_combo.grid(row=0, column=1, padx=2, pady=2, sticky=TK.EW)
        conf_btn_add.grid(row=0, column=3, padx=2, pady=2)
        conf_btn_del.grid(row=0, column=4, padx=2, pady=2)
        help_btn.grid(row=0, column=6, padx=2, pady=2, sticky=TK.E)
        about_btn.grid(row=0, column=7, padx=2, pady=2, sticky=TK.E)

        return frame

    def __init_top_frame(self, parent):
        frame = TK.Frame(parent)
        frame.columnconfigure(1, weight=1)

        self.files = {}
        for i in range(n_file_entries):
            var_use_flag = TK.BooleanVar()
            var_path = TK.StringVar()
            var_offset = TK.StringVar()

            file_chbx = TK.Checkbutton(frame, variable=var_use_flag,
                                       command=SLOT(self.update_file_entry_state, i))
            file_path = TK.Label(frame, relief=TK.SUNKEN,
                                 textvariable=var_path,
                                 activebackground='white',
                                 anchor=TK.W, state=TK.DISABLED)
            file_btn = TK.Button(frame, text="...",
                                 command=SLOT(self.get_file_name, i),
                                 state=TK.DISABLED)
            file_offset_label = TK.Label(frame, text="Offset:",
                                         state=TK.DISABLED)
            file_offset = TK.Entry(frame, width=12, textvariable=var_offset,
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

        return frame

    def __init_mid_frame(self, parent):
        frame = TK.Frame(parent, relief=TK.RIDGE, bd=3)
        frame.columnconfigure(6, weight=1)

        self.var_port_value = TK.StringVar()
        self.var_flash_freq = TK.StringVar()
        self.var_flash_mode = TK.StringVar()
        self.var_flash_size = TK.StringVar()

        port_label = TK.Label(frame, text="Port:")
        port_value = TK.Entry(frame, textvariable=self.var_port_value, width=12)

        style = TTK.Style()
        # style.map('TCombobox', selectbackground=[('readonly', 'red')])
        style.map('TCombobox', fieldbackground=[('readonly', 'white')])

        combo_width = 12

        flash_freq_label = TK.Label(frame, text="Flash freq:")
        flash_freq = TTK.Combobox(frame, textvariable=self.var_flash_freq,
                                  width=combo_width, state='readonly',
                                  values=list_flash_frequencies)
        flash_mode_label = TK.Label(frame, text="Flash mode:")
        flash_mode = TTK.Combobox(frame, textvariable=self.var_flash_mode,
                                  width=combo_width, state='readonly',
                                  values=list_flash_modes)
        flash_size_label = TK.Label(frame, text="Flash size:")
        flash_size = TTK.Combobox(frame, textvariable=self.var_flash_size,
                                  width=combo_width, state='readonly',
                                  values=list_flash_sizes)

        flash_btn = TK.Button(frame, text="Flash", command=self.__execute)
        clear_log_btn = TK.Button(frame, text="Clear log",
                                  command=self.__clear_log)

        port_label.grid(row=0, column=0, padx=2, sticky=TK.W)
        port_value.grid(row=0, column=1, padx=2, sticky=TK.W)
        flash_btn.grid(row=0, column=8, padx=10, pady=5, sticky=TK.E)

        flash_freq_label.grid(row=1, column=0, padx=2)
        flash_freq.grid(row=1, column=1, padx=2)
        flash_mode_label.grid(row=1, column=2, padx=2)
        flash_mode.grid(row=1, column=3, padx=2)
        flash_size_label.grid(row=1, column=4, padx=2)
        flash_size.grid(row=1, column=5, padx=2)
        clear_log_btn.grid(row=1, column=8, padx=10, pady=5, sticky=TK.E)

        return frame

    def __init_bot_frame(self, parent):
        frame = TK.Frame(parent)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)

        # shell and scroll
        shell_label = TK.Label(frame, text="Shell log:", anchor=TK.NW)
        self.shell = TK.Text(frame, height=20)
        scrollbar = TK.Scrollbar(frame, orient=TK.VERTICAL,
                                      command=self.shell.yview)
        self.shell.configure(yscrollcommand=scrollbar.set)

        shell_label.grid(row=0, column=0, padx=2, pady=2, sticky=TK.W)
        self.shell.grid(row=1, column=0, sticky=TK.NSEW)
        scrollbar.grid(row=1, column=1, sticky=TK.NS)

        # status bar
        self.statusbar = TK.Label(frame, text="Ready...", anchor=TK.W)
        self.statusbar.after(5000, self.clear_status_bar)
        self.statusbar.grid(row=2, column=0, sticky=TK.EW)

        return frame

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
        #                 "The message header...",
        #                 "The question...?", parent=self.parent)
        # if reply is None:
        #     return False
        # if reply:
        #     return self.doRequiredAction()
        return True

    def __update_fe(self, entry, enabled):
        entry[key_w_btn].config(state=TK.ACTIVE if enabled else TK.DISABLED)
        entry[key_w_path].config(state=TK.ACTIVE if enabled else TK.DISABLED)
        entry[key_w_offset_lbl].config(state=TK.ACTIVE if enabled else TK.DISABLED)
        entry[key_w_offset].config(state=TK.NORMAL if enabled else TK.DISABLED)

    def __reset_offset(self, var_offset):
        var_offset.set('0x')

    def __combo_config_name_set(self, name):
        self.var_conf_combo.set(name)

    def __combo_config_name_get(self):
        return self.var_conf_combo.get()

    def __port_get(self):
        return self.var_port_value.get()

    def __port_set(self, val):
        self.var_port_value.set(val)

    def __save_settings(self):
        current_conf = self.__combo_config_name_get()
        self.S.save_conf_file_entries(current_conf, self.files)

        # general
        general_settings = {
            key_port: self.__port_get(),
            key_conf_current_set_name: current_conf,

            key_flash_freq: self.var_flash_freq.get(),
            key_flash_mode: self.var_flash_mode.get(),
            key_flash_size: self.var_flash_size.get(),
        }
        self.S.save_general_settings(general_settings)

        # save on disk
        self.S.write()

    def __read_settings(self):
        # fill file entries
        self.__fill_fes()

        # general
        general_settings = self.S.general_settings()
        self.__port_set(general_settings[key_port])
        self.__combo_config_name_set(general_settings[key_conf_current_set_name])

        self.var_flash_freq.set(general_settings[key_flash_freq])
        self.var_flash_mode.set(general_settings[key_flash_mode])
        self.var_flash_size.set(general_settings[key_flash_size])

        # fill combo with configurations list
        self.conf_combo['values'] = self.S.configurations()

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
        self.S.remove_conf(config_name)
        self.__save_settings()

    def __combo_clicked(self, *a):
        self.__fill_fes(self.__combo_config_name_get())

    def __execute(self):
        parts = [(fe[key_v_part_offset].get(), fe[key_v_part_path].get())
                    for fe in self.files.values()
                        if fe[key_v_part_use_flag].get()]
        self.executor.run(parts, out=self.shell, port=self.__port_get())

    def __clear_log(self):
        self.shell.delete(1.0, TK.END)

    def __help(self):
        self.executor.help(self.shell)

    def __about(self):
        wnd_about(self.parent)
