#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
"""

__author__ = 'remico <remicollab+github@gmal.com>'

import subprocess
import tkinter as TK
from re import escape as _escape

class Executor:
    def __init__(self):
        self.tool =  self.esptool_path()

    def esptool_path(self):
        p = subprocess.Popen('which esptool.py', shell=True,
                             stdout=subprocess.PIPE, universal_newlines=True)
        return p.stdout.readline()[:-1]

    def run(self, parts, *, out=None, port=None):
        port_ = port if port is not None else "/dev/ttyUSB0"
        parts_ = ' '.join(("%s %s" % (fe[0], _escape(fe[1])) for fe in parts))

        command = "{tool} --port={port} write_flash {bins}"\
                   .format(tool=self.tool, port=port_, bins=parts_)

        try:
            o_ = subprocess.check_output(command, shell=True,
                                         universal_newlines=True)
            if out is not None:
                out.insert(TK.END, o_)
        except subprocess.CalledProcessError as e:
            if out is not None:
                out.insert(TK.END, str(e) + "\n")
                out.insert(TK.END, str(e.output) + "\n")
