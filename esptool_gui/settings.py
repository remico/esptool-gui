#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""The application's settings module
"""

__author__ = 'remico <remicollab+github@gmal.com>'

import os.path
import re
from .constants import *
from configparser import ConfigParser
from functools import partial


def _conf_full(conf):
    return key_conf_prefix + conf


class INISettings:
    def __init__(self):
        self.sfname = 'espsettings.ini'
        if not os.path.exists(self.sfname):
            with open(self.sfname, mode='w+'): pass

        self.conf = ConfigParser()
        self.conf.read(self.sfname)

    def write(self):
        with open(self.sfname, 'w') as f:
            self.conf.write(f)

    def remove_conf(self, conf):
        self.conf.remove_section(_conf_full(conf))

    def __option_set(self, section, option, value):
        c = self.conf
        if not c.has_section(section):
            c.add_section(section)
        c.set(section, option, str(value))

    def __option_get(self, section, option, type=str):
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

    def __current_config(self):
        return self.__option_get(key_conf_sec_general, key_conf_current_set_name)

    def configurations(self):
        return [conf[len(key_conf_prefix):]
                    for conf in self.conf.sections()
                        if conf.startswith(key_conf_prefix)]

    def conf_file_entries(self, conf=None):
        curr = _conf_full(conf if conf is not None else self.__current_config())
        entries = {}
        if curr not in self.conf.sections():
            return entries
        for opt in self.conf.options(curr):
            if re.search(r"(?:^\d+\.\w+$)", opt) is not None:
                key_fe, key_opt = opt.split('.')
                fe = entries.setdefault(int(key_fe), {})
                fe[key_opt] = self.__option_get(curr, opt,
                                bool if key_opt == key_v_part_use_flag else str)
        return entries

    def save_conf_file_entries(self, conf, entries):
        sec = _conf_full(conf)
        for k, fe in entries.items():
            mkopt = lambda opt: '.'.join((str(k), opt))
            self.__option_set(sec, mkopt(key_v_part_path), fe[key_v_part_path].get())
            self.__option_set(sec, mkopt(key_v_part_offset), fe[key_v_part_offset].get())
            self.__option_set(sec, mkopt(key_v_part_use_flag), str(bool(fe[key_v_part_use_flag].get())))

    def last_used_path(self, conf):
        return self.__option_get(_conf_full(conf), key_conf_last_dir)

    def save_last_used_path(self, conf, path):
        self.__option_set(_conf_full(conf), key_conf_last_dir, path)

    def general_settings(self):
        opt = partial(self.__option_get, key_conf_sec_general)
        return {
            key_port: opt(key_port),
            key_conf_current_set_name: self.__current_config() if self.__current_config() else default_conf_sec_name,
            key_flash_mode: opt(key_flash_mode),
            key_flash_freq: opt(key_flash_freq),
            key_flash_size: opt(key_flash_size),
        }

    def save_general_settings(self, data):
        for opt, val in data.items():
            self.__option_set(key_conf_sec_general, opt, val)
