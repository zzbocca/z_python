import time
import threading
import schedule
import queue
from lib import MyParser
from lib.MyDebug import Dprint as dprint
from datetime import datetime
import pytz

class MySchd:
    def __init__(self, tel):
        self.que = queue.Queue()
        self.sch_thread()
        self.work_thread()
        self.tel = tel

    def __del__(self):
        self.que.clear()

    def work_thread(self):
        self.wthd = threading.Thread(target=self.work_parse)
        self.wthd.start()

    def sch_thread(self):
        self.sthd = threading.Thread(target=self.work_schd)
        self.sthd.start()

    def add_schedule(self, parser):
        now_start = 0
        dprint("add sch")
        sec_str = parser.get_sch_timeout()
        if len(sec_str) > 1 and sec_str.find(":") != -1:
            FMT = '%H:%M'
            ntime = time.localtime()
            ctime = time.strftime(FMT, ntime)
            dtime = datetime.strptime(sec_str, FMT) - datetime.strptime(ctime, FMT)
            dstime = int(dtime.total_seconds())
            print(dstime)
            if dstime > 0:
                sec = dstime
            else:
                sec = 86400 + dstime
            if dstime == 0:
                now_start = 1
        else:
            sec = int(sec_str)
            if sec > 0:
                now_start = 1

        dprint("timeout sec = " + str(sec), 2)
        if now_start == 1:
            self.que.put(parser)
            dprint("start sch")

        if sec > 0:
            dprint("do start")
            return schedule.every(sec).seconds.do(self.que.put, parser)
        else:
            parser.set_sch_timeout("0")
            return None

    def del_schedule(self, event):
        dprint("delete event")
        schedule.cancel_job(event)

    def work_parse(self):
        while 1:
            #with self.que.mutex:
            if self.que.empty() is True:
                time.sleep(1)
            else:
                dprint("get parser")
                parser = self.que.get()
                parser.parse_start(self.tel)
                self.que.task_done()

    def work_schd(self):
        while 1:
            schedule.run_pending()
            time.sleep(1)
