#!/usr/bin/python3
# -*- coding: cp949 -*-

import os.path
import sys
import io
from bs4 import BeautifulSoup
import requests

from lib.MyDebug import Dprint as dprint
from lib import MyData
from lib import MyParser
from lib import MyFile

now = 0

toss_url = "https://quizbang.tistory.com/category/%ED%80%B4%EC%A6%88%20%EC%A0%95%EB%8B%B5/%ED%86%A0%EC%8A%A4%20%ED%96%89%EC%9A%B4%ED%80%B4%EC%A6%88"
cw_url = "https://quizbang.tistory.com/category/%ED%80%B4%EC%A6%88%20%EC%A0%95%EB%8B%B5/%EC%BA%90%EC%8B%9C%EC%9B%8C%ED%81%AC"
default_url = "https://quizbang.tistory.com/"

class ChungDab(MyParser.MyParser):
    def __init__(self, timeout):
        super().__init__(timeout)
        self.tel_channel = 0
        self.parser_list = []
        self.today_str =""
        self.search_url()
        self.data = MyData.MyList("./data/chungdab.txt") #data 0 : index, 1 : answer, 2 : msg_id
        self.data.load_data()
        self.data_list = self.data.get_data()

    def check_ignore(self, now):
        if now.hour == 9 and now.minute == 0:
            self.today_str = str(now.month) + "월" + str(now.day) + "일"
            self.data_default()
            self.check_default()
            dprint(self.today_str, 4)

        if self.today_str is None or len(self.today_str) == 0:
            self.today_str = str(now.month) + "월" + str(now.day) + "일"
            dprint(self.today_str, 4)

        #if now.minute >= 15 and now.minute < 30:
        #    if now.minute == 15 or now.minute == 20 or now.minute == 25:
        #        return 0
        #    else:
        #        return 1
        #elif now.minute >= 45 and now.minute < 60:
        #    if now.minute == 15 or now.minute == 20 or now.minute == 25:
        #        return 0
        #    else:
        #        return 1
        #else:
        #    return 0

    def search_url(self):
        self.set_url(toss_url)
        self.set_url(cw_url)

    def search_parser(self, index):
        for p in self.parser_list:
            if p.index == index:
                return p
        return None

    def parse_data(self, url):
        global cw_url
        global default_url

        self.ret_list.clear()

        with requests.Session() as s:
            res = s.get(url)
            if res.status_code == requests.codes.ok:
                soup = BeautifulSoup(res.text, "lxml")
                index = 1
                dprint(res.text, 9)
                if url == cw_url:
                    target = 10
                else:
                    target = 2

                while index < target:
                    result = soup.select_one("#content > div.inner > div:nth-child(" + str(index) + ") > a")
                    list_ref = result['href']
                    list_index = int(list_ref[1:5])
                    dprint(list_index, 8)

                    result = soup.select_one("#content > div.inner > div:nth-child(" + str(index) + ") > a > span.title")
                    dprint(self.today_str, 8)
                    tmp_index = result.text.find(self.today_str)
                    if tmp_index == -1:
                        break
                    start_index = tmp_index + len(self.today_str)

                    name = result.text[start_index:]
                    dprint(name, 8)

                    if self.search_parser(list_index) is None:
                        target_url = default_url + str(list_index)
                        if target == 2:
                            toss = Toss(name, list_index, target_url)
                            self.parser_list.append(toss)
                        else:
                            cw = CashWalk(name, list_index, target_url)
                            self.parser_list.append(cw)

                    index = index + 1

            for sub in self.parser_list:
                for url in sub.url_list:
                    sub.parse_data(url)
                    if len(sub.ret) != 0:
                        dprint(sub.ret, 2)
                        self.ret_list.append(sub)

    def parse_start(self, tel):
        dprint()
        if self.check_current() == 0:
            return
        dprint(self.url_list)
        for url in self.url_list:
            dprint(url, 3)
            if len(url) > 0:
                self.parse_data(url)
                if self.ret_list is not None and len(self.ret_list) > 0:
                    for ret_obj in self.ret_list:
                        print(ret_obj.ret)
                        ret_obj.msg_id = tel.send_answer(ret_obj.ret, self.tel_channel, ret_obj.msg_id)

class AnswerSub(MyParser.MyParser):
    def __init__(self, name, title, index, url):
        super().__init__()
        self.index = 0
        self.name = name
        self.title = title
        self.index = index
        self.answer = ""
        self.set_url(url)

    def __exit__(self, exc_type, exc_val, exc_tb):
        super(AnswerSub, self).__exit__(exc_type, exc_val, exc_tb)

    def parse_sub(self, soup):
        pass

    def get_answer(self):
        return self.answer

    def parse_data(self, url):

        if self.check_current() == 0:
            return

        self.ret = ""

        dprint("parse url :" + url, 8)

        with requests.Session() as s:
            res = s.get(url)
            smessage = str(self.index) + " " + self.name
            dprint(smessage, 8)
            if res.status_code == requests.codes.ok:
                soup = BeautifulSoup(res.text, "lxml")

                answer_data = self.parse_sub(soup)
                if answer_data is None or len(answer_data) == 0:
                    return

                dprint(answer_data, 5)
                if self.answer == answer_data:
                    return

                self.answer = answer_data
                dprint('index = %d value = %s.' % (self.index, self.answer), 5)
                smessage = smessage + self.answer + " " + url

                self.ret = smessage
                dprint(smessage, 8)
        dprint(self.ret, 7)
    
class Toss(AnswerSub):
    def __init__(self, title, index, url):
        super(Toss, self).__init__("[토스]", title, index, url)

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def parse_sub(self, soup):
        all_red = ""
        count = 0

        title = soup.find(text="[ 토스 정답 모음 ]")
        title_ppp = title.parent.parent.parent

        while count < 15:
            next = title_ppp.nextSibling
            if len(str(next)) > 10:
                ret = next.span
                value = str(ret)
                dprint(len(value), 8)
                if len(value) < 300:
                    if value.find("#ee2323") != -1 or value.find("#EE2323") != -1 or value.find("rgb(238, 35, 35)") != -1:
                        red = ret.text
                        dprint(red, 8)
                        if red.find("공유") == -1:
                            all_red += red + " "
            title_ppp = next
            count = count + 1
            dprint(count, 8)

        dprint(all_red, 7)
        return all_red


class CashWalk(AnswerSub):
    def __init__(self, title, index, url):
        super(CashWalk, self).__init__("[캐시워크]", title, index, url)

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def parse_sub(self, soup):
        answer = ""
        result = soup.find(text="▶퀴즈 정")
        dprint(result, 8)
        if result is None:
            return answer
        par1 = result.parent
        par2 = par1.parent
        value = par2.parent
        spans = value.find_all("span")
        answer_data = spans[2].text

        if answer_data[0] == ':' and len(answer_data) < 3:
            dprint("wrong date %s" % answer_data)
        elif answer_data[1] == ':' and len(answer_data) < 4:
            dprint("wrong date %s" % answer_data)
        elif answer_data.find("공유") == -1:
            answer = answer_data

        return answer

