#!/usr/bin/python3
# -*- coding: cp949 -*-

from bs4 import BeautifulSoup
import requests
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from lib.MyDebug import Dprint as dprint
from lib import MyParser
from lib import MyBdriver
from lib import MyData

now = 0

search_url = "https://quasarzone.com/groupSearches?page=1&group_id=qsz_deal&kind=nick&keyword=%EC%95%84%EB%A6%AC%EC%8B%9C%EC%95%84&basekind=subject%7C%7Ccontent&baseword=#none"
default_url = "https://quasarzone.com"


class Naverpay(MyParser.MyParser):
    def __init__(self, timeout):
        super().__init__(timeout, send_to_ch=1)
        self.now = None
        self.now_date_hip = ""
        self.parser_list = []
        self.today_str = ""
        self.search_url()
        self.login = MyData.MyList("./data/naver_login.txt")
        self.login.load_data()
        self.login_list = self.login.get_data()
        self.last_index = 0

    def check_valid_time(self):
        now_time = super(Naverpay, self).check_valid_time()

        if now_time is not None:
            self.now = now_time
            self.now_date_hip = "%d-%02d-%02d" % (self.now.year, self.now.month, self.now.day)
        else:
            self.now = None

        return self.now

    def do_enable(self):
        self.clear_url_list()
        self.parser_list.clear()
        self.search_url()

    def do_disable(self):
        self.clear_url_list()
        self.parser_list.clear()

    def search_url(self):
        self.set_url(search_url)

    def search_parser(self, index):
        for p in self.parser_list:
            if p.index == index:
                return p
        return None

    def parse_data(self, url=""):
        global default_url
        self.ret_list.clear()

        with requests.Session() as s:
            res = s.get(url)
            if res.status_code == requests.codes.ok:
                soup = BeautifulSoup(res.text, "lxml")
                dprint(res.text, 9)
                index = 1
                latest_index = 0
                while index <= 5:
                    selector = "#content > div.sub-content-wrap > div.left-con-wrap.search-width855 > div.total-search-list-wrap > div.srch-area > dl > dd > ul > li:nth-child(" + str(index) + ") > div.cont-wrap > div.sub-cont-wrap > p.time"
                    result = soup.select_one(selector)
                    if result is not None and result.text != self.now_date_hip:
                        break
                    selector = "#content > div.sub-content-wrap > div.left-con-wrap.search-width855 > div.total-search-list-wrap > div.srch-area > dl > dd > ul > li:nth-child(" + str(index) + ") > div.cont-wrap > div.tit-cont-wrap > p.title > a"
                    result = soup.select_one(selector)

                    if result is not None:
                        total_chart = 0

                        ref = result['href']
                        find_index = ref.find("views/")
                        if find_index == -1:
                            return

                        chart_index = int(ref[find_index+6:])
                        dprint("chart index = %d"%chart_index, 3)
                        if index == 1:
                            if self.last_index == chart_index:
                                break
                            latest_index = chart_index
                        dprint("latest_index = %d self.last_index = %d"%(latest_index,self.last_index), 3)
                        if chart_index <= self.last_index:
                            break
                        if result.text.find("종합 차트") != -1:
                            total_chart = 1

                        target_url = default_url + result['href']
                        answer = AnswerSub(target_url, total_chart, self.login_list)
                        self.parser_list.append(answer)

                    index += 1
                    self.last_index = latest_index

        for sub in self.parser_list:
            for url in sub.url_list:
                sub.parse_data(url)
                if len(sub.ret) != 0:
                    dprint(sub.ret, 2)
                    self.ret_list.append(sub)

    def parse_start(self, tel):
        if self.check_current() == 0:
            return
        for url in self.url_list:
            dprint(url, 3)
            if len(url) > 0:
                self.parse_data(url)
                if self.ret_list is not None and len(self.ret_list) > 0:
                    for ret_obj in self.ret_list:
                        if ret_obj.ret_list is not None and len(ret_obj.ret_list) > 0:
                            for ret in self.ret_list:
                                tel.send_answer(ret, self.send_result_to_ch)
                        elif ret_obj.ret is not None and len(ret_obj.ret):
                            tel.send_answer(ret_obj.ret, self.send_result_to_ch)


class AnswerSub(MyParser.MyParser):
    def __init__(self, url, total_chart=0, login_list=None):
        super().__init__()
        self.answer = ""
        self.my_d = MyBdriver.myBdriver()
        self.driver = self.my_d.getDriver()
        self.login_url = 'https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com'
        self.set_url(url)
        self.id_list = []
        self.total_chart = total_chart
        self.login_list = login_list

    def get_answer(self):
        return self.answer

    def login_naver_with_execute_script(self, userid, userpw):
        script = "(function execute(){ document.querySelector('#id').value = '" + userid + "'; document.querySelector('#pw').value = '" + userpw + "';})();"
        self.driver.execute_script(script)

        self.driver.find_element_by_id("log.login").click()
        return False

    def parse_data(self, url=""):
        dprint()
        if self.check_current() == 0:
            return
        dprint()
        self.ret = ""

        if self.answer != url:
            self.answer = url
        else:
            return

        dprint("parse url :" + url, 8)

        for login in self.login_list:
            # naver login
            userid = login[0]
            userpw = login[1]

            with requests.Session() as s:
                self.driver.implicitly_wait(1)
                self.driver.get(self.login_url)
                self.login_naver_with_execute_script(userid, userpw)

                self.ret_list.clear()
                self.driver.get(url)

                search_str = self.driver.find_elements_by_xpath('//*[@id="new_contents"]/p[*]/a')
                len_str = len(search_str)
                index = 0
                for ref in search_str:
                    if index < len_str:
                        if ref.text.find("click-point") != -1:
                            self.ret_list.append(ref.text)
                            dprint(ref.text, 5)
                        elif ref.text.find("ofw") != -1:
                            break
                    index += 1

                for ret_url in self.ret_list:
                    dprint(ret_url)
                    self.driver.get(ret_url)
                    try:
                        WebDriverWait(self.driver, 3).until(EC.alert_is_present(), 'Timed out waiting for PA creation confirmation popup to appear.')
                        alert = self.driver.switch_to_alert()
                        alert.accept()
                        dprint("alert accepted", 8)
                    except TimeoutException:
                        dprint("no alert", 8)

                    dprint("getting ok", 2)
