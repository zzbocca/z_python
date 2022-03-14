#!/usr/bin/python3
# -*- coding: cp949 -*-

import sys
import io
import os.path
import json
from lib import MyDebug

class MyFile:
    def __init__(self, fname):
        self.fname = fname
        self.type = "none"

    def set_type(self, type):
        self.type = type

    def read(self):
        if os.path.isfile(self.fname):
            if self.type == "json":
                with open(self.fname, 'r') as filehandle:
                    return json.load(filehandle)

    def write(self, value):
        MyDebug.Dprint(value)
        if self.type == "none":
            f = open(self.fname, mode='at', encoding='utf-8')
            f.write(value)
            f.write("굈")
            f.close()
        elif self.type == "json":
            with open(self.fname, 'w') as filehandle:
                json.dump(value, filehandle)