#!/usr/bin/python3
# -*- coding: cp949 -*-

import sys
import io
import inspect
import datetime
import pytz

myDebug = 10

def Denable(value):
    global myDebug
    myDebug = value

def get_Denable():
    global myDebug
    return myDebug

def Dprint(value="", level = 1):
    if myDebug == 0:
        return 0

    if myDebug < level:
        return 0

    callerframerecord = inspect.stack()[1]  # 0 represents this line
    # 1 represents line at caller
    frame = callerframerecord[0]
    info = inspect.getframeinfo(frame)

    print('[%s'%info.function, ':%s]'%info.lineno, value)
    return 1

def print_now():
    now = datetime.datetime.now(pytz.timezone('Asia/Seoul'))
    log_msg = "current time = "+str(now)
    Dprint(log_msg)
