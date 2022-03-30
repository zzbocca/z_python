#!/usr/bin/python3
# -*- coding: cp949 -*-

import sys
import io
import os.path
import json
from lib.MyDebug import Dprint as dprint

class MyFile:
    def __init__(self, fname):
        self.fname = fname
        self.type = "none"

    def set_type(self, type):
        self.type = type

    def exist(self):
        if os.path.exists(self.fname):
            return 1
        return 0

    def read(self):
        if os.path.isfile(self.fname):
            dprint(self.type)
            if self.type == "json":
                with open(self.fname, 'r') as filehandle:
                    return json.load(filehandle)
            elif self.type == "kjson":
                with open(self.fname, 'r', encoding='UTF-8') as filehandle:
                    return json.load(filehandle)

    def write(self, value):
        dprint(value, 10)
        if self.type == "none":
            f = open(self.fname, mode='at', encoding='utf-8')
            f.write(value)
            f.write("굈")
            f.close()
        elif self.type == "json":
            with open(self.fname, 'w') as filehandle:
                filehandle.write(json.dumps(value, indent=4))
        elif self.type == "kjson":
            with open(self.fname, 'w', encoding='UTF-8') as filehandle:
                json.dump(value, filehandle, ensure_ascii=False, indent=4)