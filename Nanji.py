# -*- coding: cp949 -*-
from dateutil.relativedelta import relativedelta
import datetime
from bs4 import BeautifulSoup
import requests
import re

from lib import MyBdriver
from lib import MyParser
from lib.MyDebug import Dprint as dprint
from lib import MyData

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"}

reserv_url_1 = "https://yeyak.seoul.go.kr/web/reservation/selectReservView.do?rsv_svc_id="
reserv_url_2 = "&code=T500&dCode=T502&sch_order=1&sch_choose_list=&sch_type=&sch_text=&sch_recpt_begin_dt=&sch_recpt_end_dt=&sch_use_begin_dt=&sch_use_end_dt=&sch_reqst_value="

search_url_1 = "https://yeyak.seoul.go.kr/web/search/selectPageListDetailSearchImg.do?code=T500&dCode=T502&sch_order=3&sch_choose_list=&sch_type=&sch_text="
search_url_2 = "&sch_recpt_begin_dt=&sch_recpt_end_dt=&sch_use_begin_dt=&sch_use_end_dt="

nanji_site_name = ["B형",
                   "C형",
                   "D형",
                   "잔디",
                   "글램핑",
                   "바비큐존(4인용)",
                   "바비큐존(8인용)",
                   "바비큐존(12인용)"]

class Nanji(MyParser.MyParser):
    def __init__(self, timeout):
        super(Nanji, self).__init__(timeout)
        self.month_list = []
        self.now_date = 0
        self.now = None
        self.my_d = MyBdriver.myBdriver()
        self.driver = self.my_d.getDriver()
        self.site_data = MyData.MyDict("./data/naji.text", "kjson")
        self.site_dict = self.site_data.get_data()
        self.update_data(True)
        self.get_reserve_url()

    def __del__(self):
        super(Nanji, self).__del__()
        if hasattr(Nanji, 'my_d'):
            self.my_d.temDriver()

    def check_valid_time(self):
        now = super(Nanji, self).check_valid_time()
        if now is not None:
            self.now = now
            if now.day != self.now.day:
                if self.update_data(False) == 1:
                    self.get_reserve_url()
        else:
            self.now = None

    def search_url_parse(self, url):
        dprint(url)
        page_id = None
        with requests.Session() as s:
            res = s.get(url)
            if res.status_code == requests.codes.ok:
                soup = BeautifulSoup(res.text, 'lxml')
                properties = soup.findAll('a', onclick=True)
                for x in properties:
                    if re.match('fnDetailPage', x['onclick']):
                        page_id = x['onclick'][14:33]
                        break

        dprint(page_id, 4)
        return page_id

    def get_now_month(self):
        if self.now is None:
            self.now = datetime.datetime.today()
        self.month_list.clear()
        self.month_list.append(self.now.month)
        self.now_date = self.now.year * 10000 + self.now.month * 100 + self.now.day

        if self.now.day > 15:
            after_month = self.now + relativedelta(months=1)
            self.month_list.append(after_month.month)

    def update_data(self, from_file):
        global nanji_site_name
        diff = 0
        update = 0
        self.get_now_month()
        dprint(id(self.site_dict))
        if from_file == 1 and self.site_data.load_data() == 0:
            for mon in self.month_list:
                for site_name in nanji_site_name:
                    url_key = str(mon) + "월%20" + str(site_name)
                    self.site_dict[url_key] = ["", {}]
                    diff = 1
            dprint(self.site_dict, 11)
        else:
            dprint(self.site_dict, 9)
            for key, value in self.site_dict.items():
                month = self.month_list[0]
                index = key.find("월")
                if index < 0:
                    continue
                saved_month = int(key[0:index])
                if month >= 12 and saved_month == 1:
                    pass
                else:
                    if saved_month < month:
                        self.site_dict.remove(key)
                        diff = 1
                        update = 0
                    else:
                        if len(value[1]) != 0:
                            for date in value[1].keys():
                                if int(date) < self.now_date:
                                    value[1].remove(date)
                                    diff = 1

        if diff == 1:
            self.site_data.save_data()

        if update == 1:
            self.clear_url_list()
            return 1

        return 0

    def get_reserve_url(self):
        diff = 0
        if self.timeout == 0:
            return

        for key, value in self.site_dict.items():
            if len(value[0]) == 0:
                url = search_url_1+key+search_url_2
                value[0] = self.search_url_parse(url)
                diff = 1

            if len(value[1]) != 0:
                url = reserv_url_1+value[0]+reserv_url_2
                self.set_url(url)

        if diff == 1:
            self.site_data.save_data()
        dprint(self.url_list, 1)

    def parse_data(self, url):
        dprint(url)

        with requests.Session() as s:
            self.driver.get(url)
            title = self.driver.find_element_by_xpath('//*[@id="aform"]/div[1]/h4/span[1]').text
            dprint(title)
            for key, value in self.site_dict.items():
                if title.find(key) != -1:
                    for date in value.keys():
                        id_str = "div_cal_" + date
                        dprint("id_str = " + id_str, 4)
                        data = self.driver.find_element_by_id(id_str)
                        dprint(str(date) + " reserved : " + data.text)
                        if data.text[2] == "/":
                            remine = data.text[0:2]
                            total = data.text[3:5]
                        else:
                            remine = data.text[0]
                            total = data.text[2]
                        dprint(remine + "  " + total, 4)
                        avail_value = int(total) - int(remine)
                        if avail_value != 0:
                            result = key + " " + str(date) + " 잔여수량 : " + str(avail_value)
                            self.ret_list.append(result)

