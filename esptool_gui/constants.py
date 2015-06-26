#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
"""

__author__ = 'remico <remicollab+github@gmal.com>'


app_name = "esptool GUI"
app_version = "0.1.0a"
app_developer = "remico"
app_developer_email = "remicollab+dev@gmail.com"
app_url = "https://github.com/remico/esptool-gui"


n_file_entries = 8


key_v_part_use_flag = 'used'
key_v_part_path = 'path'
key_v_part_offset = 'offset'

key_w_use_flag = 'w_used'
key_w_path = 'w_path'
key_w_btn = 'w_btn'
key_w_offset_lbl = 'w_offset_lbl'
key_w_offset = 'w_offset'


key_conf_sec_general = "General"
key_conf_prefix = "Config+"
default_conf_sec_name = "Default"
key_conf_sec_default = key_conf_prefix + default_conf_sec_name


key_conf_last_dir = "lastdir"
key_conf_current_set_name = "current"
key_port = "port"
key_flash_size = "flashsize"
key_flash_mode = "flashmode"
key_flash_freq = "flashfreq"


list_flash_modes = ['qio', 'qout', 'dio', 'dout']
list_flash_frequencies = ['40m', '26m', '20m', '80m']
list_flash_sizes = ['8m','2m','4m','16m','32m','16m-c1','32m-c1','32m-c2']
