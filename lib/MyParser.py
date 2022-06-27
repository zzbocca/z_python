

import datetime
import pytz
from lib.MyDebug import Dprint as dprint


class MyParser:
    def __init__(self, timeout=60, send_to_ch = 0):
        self.check_time = 0
        self.start_h = 0
        self.end_h = 0
        self.timeout = timeout
        self.ret_list = []
        self.ret = ""
        self.url_list = []
        self.msg_id = 0
        self.tel = None
        self.cmd_list = {}
        self.schd_event=None
        self.send_result_to_ch = send_to_ch

    def __del__(self):
        self.ret_list.clear()
        self.url_list.clear()
        self.cmd_list.clear()

    def get_name(self):
        return type(self).__name__

    def set_Telegram(self, tel):
        self.tel = tel

    def get_cmd_list(self):
        return self.cmd_list

    def add_cmd(self, cmd, func, desc):
        if cmd is None or func is None:
            return
        if desc is not None and len(desc) != 0:
            self.cmd_list[cmd] = desc
        else:
            self.cmd_list[cmd] = ""
        self.tel.add_handler(cmd, func)

    def set_sch_timeout(self, msec):
        if self.timeout == msec:
            return
        elif self.timeout == 0 and msec != 0:
            self.do_enable()
        else:
            self.do_disable()

        self.timeout = msec

    def do_enable(self):
        pass

    def do_disable(self):
        pass

    def get_sch_timeout(self):
        return self.timeout

    def help(self, update, context):
        pass

    def set_valid_time(self, start_h, end_h):
        if start_h == end_h:
            return False
        if start_h > 24 or start_h < 0 or end_h > 24 or end_h < 0:
            return False
        if start_h == 0 and end_h == 24:
            return False
        if end_h == 0 and start_h == 24:
            return False

        self.check_time = 1
        self.start_h = start_h
        self.end_h = end_h
        return True

    def check_valid_time(self):
        now = datetime.datetime.now(pytz.timezone('Asia/Seoul'))
        if self.check_time == 0:
            dprint(now, 2)
            return now

        if now.hour >= self.start_h and now.hour <= self.end_h:
            return now

        return None

    def check_ignore(self, now):
        return 0

    def search_url(self):
        pass

    def check_url(self, url):
        for ref in self.url_list:
            if ref == url:
                return 1

        return 0

    def set_url(self, url):
        if self.check_url(url) == 0:
            dprint(url,8)
            self.url_list.append(url)

    def clear_url(self, url):
        if self.check_url(url) == 1:
            self.url_list.remove(url)

    def clear_url_list(self):
        self.url_list.clear()

    def get_url_len(self):
        return len(self.url_list)

    def parse_data(self, url=""):
        pass

    def check_current(self):
        now = self.check_valid_time()
        if now is None:
            return 0
        if self.check_ignore(now) == 1:
            return 0
        return 1

    def parse_start(self, tel):
        #sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')
        #sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
        if self.check_current() == 0:
            return
        dprint(self.url_list)
        for url in self.url_list:
            dprint(url, 3)
            if len(url) > 0:
                self.parse_data(url)
                if self.ret is not None and len(self.ret) != 0:
                    dprint(self.ret, 1)
                    tel.send_answer(self.ret, to_chan=self.send_result_to_ch)
                elif self.ret_list is not None and len(self.ret_list) > 0:
                    dprint(self.ret_list, 1)
                    for ret in self.ret_list:
                        tel.send_answer(ret, to_chan=self.send_result_to_ch)



