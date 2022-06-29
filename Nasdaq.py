
import os.path
from bs4 import BeautifulSoup
import requests
from lib.MyDebug import Dprint as dprint
from lib import MyParser
from datetime import datetime
import time

class Nasdaq(MyParser.MyParser):
    def __init__(self, timeout):
        super(Nasdaq, self).__init__(timeout, send_to_ch=2, disable_preview='False')
        self.set_url("https://m.search.naver.com/search.naver?sm=tab_hty.top&where=m&query=%EB%82%98%EC%8A%A4%EB%8B%A5+%EC%84%A0%EB%AC%BC&oquery=nasdaq&tqi=hrqPiwprvOsssfm137Nssssssbh-411173")
        self.day = 0
        self.firstofday = 0
        self.set_valid_time(8, 16)

    def __del__(self):
        super().__del__()

    def check_ignore(self, now):
        if self.day == 0:
            self.day = now.day

        if self.day != now.day and now.hour >= 8:
            self.firstofday = 1
            self.day = now.day
        else:
            self.firstofday = 0

    def parse_data(self, url):
        self.ret_list.clear()
        if self.firstofday == 0:
            current_datetime = datetime.utcnow()
            current_timetuple = current_datetime.utctimetuple()
            current_timestamp = time.mktime(current_timetuple)
            cur_time = int(current_timestamp - 5 * 60 * 60 - 601) * 1000
            grap = "https://ssl.pstatic.net/imgfinance/chart/mobile/world/day/NQcv1_end.png?" + str(cur_time)

            self.ret_list.append(grap)
        else:
            with requests.Session() as s:
                res = s.get(url)
                if res.status_code == requests.codes.ok:
                    soup = BeautifulSoup(res.text, 'lxml')
                    #print(soup.text)






