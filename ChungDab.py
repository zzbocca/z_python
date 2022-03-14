#!/usr/bin/python3
# -*- coding: cp949 -*-

import os.path
import sys
import io
from bs4 import BeautifulSoup
import requests

from lib import MyDebug
from lib import MyParser
from lib import MyFile

now = 0

toss_url = "https://quizbang.tistory.com/category/%ED%80%B4%EC%A6%88%20%EC%A0%95%EB%8B%B5/%ED%86%A0%EC%8A%A4%20%ED%96%89%EC%9A%B4%ED%80%B4%EC%A6%88"
cw_url = "https://quizbang.tistory.com/category/%ED%80%B4%EC%A6%88%20%EC%A0%95%EB%8B%B5/%EC%BA%90%EC%8B%9C%EC%9B%8C%ED%81%AC"
default_url = "https://quizbang.tistory.com/"

class ChungDab(MyParser.MyParser):
    def __init__(self):
        super().__init__()
        self.parser_list = []
        self.today_str =""
        self.search_url()

    def check_ignore(self, now):
        if now.hour == 9 and now.minute == 0:
            self.today_str = str(now.month) + "월" + str(now.day) + "일"
            self.data_default()
            self.check_default()
            MyDebug.Dprint(self.today_str)

        if self.today_str is None or len(self.today_str) == 0:
            self.today_str = str(now.month) + "월" + str(now.day) + "일"
            MyDebug.Dprint(self.today_str)

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

        with requests.Session() as s:
            res = s.get(url)
            if res.status_code == requests.codes.ok:
                soup = BeautifulSoup(res.text, "lxml")
                index = 1
                #MyDebug.Dprint(res.text)
                if url == cw_url:
                    target = 10
                else:
                    target = 2

                while index < target:
                    result = soup.select_one("#content > div.inner > div:nth-child(" + str(index) + ") > a")
                    list_ref = result['href']
                    list_index = int(list_ref[1:5])
                    MyDebug.Dprint(list_index)

                    result = soup.select_one("#content > div.inner > div:nth-child(" + str(index) + ") > a > span.title")
                    MyDebug.Dprint(self.today_str)
                    tmp_index = result.text.find(self.today_str)
                    if tmp_index == -1:
                        break
                    start_index = tmp_index + len(self.today_str)

                    name = result.text[start_index:]
                    MyDebug.Dprint(name)

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


class AnswerSub(MyParser.MyParser):
    def __init__(self, Name, title, index, url):
        super().__init__(url)
        self.index = 0
        self.Name = Name
        self.title = title
        self.index = index
        self.answer = ""

    def __exit__(self, exc_type, exc_val, exc_tb):
        super(AnswerSub, self).__exit__(exc_type, exc_val, exc_tb)

    def parse_sub(self, soup):
        pass

    def parse_data(self, url):
        self.ret_list.clear()

        MyDebug.Dprint("parse url :" + url)

        with requests.Session() as s:
            res = s.get(url)
            smessage = str(self.index) + " " + self.Name
            MyDebug.Dprint(smessage)
            if res.status_code == requests.codes.ok:
                soup = BeautifulSoup(res.text, "lxml")

                answer_data = self.parse_sub(soup)
                if answer_data is None or len(answer_data) == 0:
                    return

                MyDebug.Dprint(answer_data)
                if self.answer == answer_data:
                    return

                self.answer = answer_data
                MyDebug.Dprint('index = %d value = %s.' % (self.index, self.answer))
                smessage = smessage + self.answer + " " + url
                self.ret_list.append(smessage)
                MyDebug.Dprint(smessage)
        MyDebug.Dprint(self.ret_list)
    
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
                MyDebug.Dprint(len(value))
                if len(value) < 300:
                    if value.find("#ee2323") != -1 or value.find("#EE2323") != -1 or value.find("rgb(238, 35, 35)") != -1:
                        red = ret.text
                        MyDebug.Dprint(red)
                        if red.find("공유") == -1:
                            all_red += red + " "
            title_ppp = next
            count = count + 1
            MyDebug.Dprint(count)

        MyDebug.Dprint(all_red)
        return all_red


class CashWalk(AnswerSub):
    def __init__(self, title, index, url):
        super(CashWalk, self).__init__("[캐시워크]", title, index, url)

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def parse_sub(self, soup):
        answer = ""
        result = soup.find(text="▶퀴즈 정")
        MyDebug.Dprint(result)
        if result is None:
            return answer
        par1 = result.parent
        par2 = par1.parent
        value = par2.parent
        spans = value.find_all("span")
        answer_data = spans[2].text

        if answer_data[0] == ':' and len(answer_data) < 3:
            MyDebug.Dprint("wrong date %s" % answer_data)
        elif answer_data[1] == ':' and len(answer_data) < 4:
            MyDebug.Dprint("wrong date %s" % answer_data)
        elif answer_data.find("공유") == -1:
            answer = answer_data

        return answer

