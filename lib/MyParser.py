
import sys
import io
import datetime
import pytz
from lib import MyDebug
from lib import MyTel

class MyParser:
    def __init__(self, default_url=""):
        self.enable = 1
        self.url_list = []
        if default_url is not None and len(default_url) != 0:
            MyDebug.Dprint("default url set (" + default_url + ")")
            self.url_list.append(default_url)
        self.check_time = 0
        self.start_h = 0
        self.end_h = 0
        self.ret_list = []

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
            return now

        if now.hour >= self.start_h and now.hour <= self.end_h:
            return now

        return None

    def check_ignore(self, now):
        return 0

    def search_url(self):
        pass

    def set_url(self, url):
        self.url_list.append(url)

    def clear_url(self, url):
        self.url_list.remove(url)

    def get_url_len(self):
        return self.url_list.len()

    def parse_data(self, url=""):
        pass


    def parse_start(self, tel):
        sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')
        sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')

        now = self.check_valid_time()
        if now is None:
            return

        if self.check_ignore(now) == 1:
            return

        for url in self.url_list:
            MyDebug.Dprint(url)
            if len(url) > 0:
                self.parse_data(url)
                MyDebug.Dprint(self.ret_list)
                if self.ret_list is not None and len(self.ret_list) > 0:
                    for ret in self.ret_list:
                        tel.send_answer(ret)



