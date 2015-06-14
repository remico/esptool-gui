#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
"""

__author__ = 'remico <remicollab+github@gmal.com>'

import subprocess
import tkinter as TK
from re import escape as _escape


class Executor:
    def __init__(self, master):
        self.master = master
        self.tool =  self.esptool_path()
        self.nextstep = 0
        self.errfile_name = 'esptoolerr'

    def esptool_path(self):
        p = subprocess.Popen('which esptool.py', shell=True,
                             stdout=subprocess.PIPE, universal_newlines=True)
        return p.stdout.readline()[:-1]

    def run(self, parts, *, out=None, port=None):
        def printout(subproc):
            while True:
                s = subproc.stdout.readline()
                if subproc.poll() is not None:
                    if not s:
                        break
                if s:
                    out.insert(TK.END, s)
                    out.see(TK.END)
                self.nextstep = self.master.after(5, next_)
                yield

        port_ = port if port is not None else "/dev/ttyUSB0"
        parts_ = ' '.join(("%s %s" % (fe[0], _escape(fe[1])) for fe in parts))

        command = "{tool} --port={port} write_flash {bins}"\
                   .format(tool=self.tool, port=port_, bins=parts_)

        try:
            p = subprocess.Popen(command, shell=True,
                                 # executable="/bin/bash",
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT,
                                 universal_newlines=True)
            if out is not None:
                next_ = printout(p).__next__
                self.nextstep = self.master.after(5, next_)

        except Exception as e:
            if out is not None:
                out.insert(TK.END, str(e) + "\n")
                out.see(TK.END)

        finally:
            if out is not None:
                out.insert(TK.END, "================ BEGIN =================\n")
