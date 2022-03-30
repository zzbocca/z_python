import time
import threading
import schedule
import queue
from lib import MyParser
from lib import MyDebug


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
        print("add sch")

        print(parser)
        sec = parser.get_sch_timeout()
        print(sec)
        if sec != 0:
            self.que.put(parser)
            print("start sch")

        if sec > 0:
            print("do start")
            print(sec)
            return schedule.every(sec).seconds.do(self.que.put, parser)

    def del_schedule(self, event):
        MyDebug.Dprint("delete event")
        schedule.cancel_job(event)

    def work_parse(self):
        while 1:
            #with self.que.mutex:
            if self.que.empty() is True:
                time.sleep(1)
            else:
                print("get parser")
                parser = self.que.get()
                print(parser)
                parser.parse_start(self.tel)
                self.que.task_done()

    def work_schd(self):
        while 1:
            schedule.run_pending()
            time.sleep(1)
