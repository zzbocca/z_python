# -*- coding: UTF-8 -*-

from telegram_bot_calendar import DetailedTelegramCalendar
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

import os.path
from dateutil.relativedelta import relativedelta
import datetime
from bs4 import BeautifulSoup
import requests
import re
import json

from lib import MyBdriver
from lib import MyParser
from lib.MyDebug import Dprint as dprint
from lib import MyData

DISPLAY_NONE=0
DISPLAY_SITE=1
DISPLAY_DATE=2
DISPLAY_DN=3
DISPLAY_DATE_UPDATE=4
SEL_NONE=0
SEL_DAY=1
SEL_NIGHT=2
SEL_ALL=3
DATE_ADD=1
DATE_DEL=2
CAL_FIRST_STR="cbcal_0_g_d_"

class Nanji(MyParser.MyParser):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"}

    reserv_url_1 = "https://yeyak.seoul.go.kr/web/reservation/selectReservView.do?rsv_svc_id="
    reserv_url_2 = "&code=T500&dCode=T502&sch_order=1&sch_choose_list=&sch_type=&sch_text=&sch_recpt_begin_dt=&sch_recpt_end_dt=&sch_use_begin_dt=&sch_use_end_dt=&sch_reqst_value="

    search_url_1 = "https://yeyak.seoul.go.kr/web/search/selectPageListDetailSearchImg.do?code=T500&dCode=T502&sch_order=3&sch_choose_list=&sch_type=&sch_text="
    search_url_2 = "&sch_recpt_begin_dt=&sch_recpt_end_dt=&sch_use_begin_dt=&sch_use_end_dt="

    booking_url_1 = "https://yeyak.seoul.go.kr/web/reservation/insertFormReserve.do?rsv_svc_id="
    booking_url_2 = "&useDe="

    nanji_site_name = ["B형",
                       "C형",
                       "D형",
                       "잔디",
                       "글램핑",
                       "바비큐존(4인용)",
                       "바비큐존(8인용)",
                       "바비큐존(12인용)",
                       "캠프파이어존(8인용)",
                       "캠프파이어존(15인용)"]

    tel_key_site = "site_"
    tel_key_date = "cbcal_0_"
    tel_key_day_night = "cb_dn_"
    tel_key_exit = "save_all"
    tel_key_sel_site = "sel_site"
    tel_key_sel_cal = "sel_cal"

    def __init__(self, timeout):
        super(Nanji, self).__init__(timeout, send_to_ch=3)
        self.month_list = []
        self.now_date = 0
        self.now = None
        self.my_d = MyBdriver.myBdriver()
        self.driver = self.my_d.getDriver()
        self.site_data = MyData.MyDict("./data/nanji.txt", "kjson")
        self.site_dict = self.site_data.get_data()
        self.update_data(True)
        self.get_reserve_url()
        self.show_msg_id = 0
        self.sel_site = ""
        self.sel_month = 0
        self.sel_date = ""
        self.send_msg = ""
        self.last_dn_date_key=""
        self.login_url = "https://yeyak.seoul.go.kr/web/loginForm.do?ru=aHR0cHM6Ly95ZXlhay5zZW91bC5nby5rci93ZWIvcmVzZXJ2YXRpb24vc2VsZWN0UmVzZXJ2Vmlldy5kbz9yc3Zfc3ZjX2lkPVMyMjA1MTMxOTA2MjM4MjU0NzcmY29kZT1UNTAwJmRDb2RlPVQ1MDImc2NoX29yZGVyPTEmc2NoX2Nob29zZV9saXN0PSZzY2hfdHlwZT0mc2NoX3RleHQ9JnNjaF9yZWNwdF9iZWdpbl9kdD0mc2NoX3JlY3B0X2VuZF9kdD0mc2NoX3VzZV9iZWdpbl9kdD0mc2NoX3VzZV9lbmRfZHQ9JnNjaF9yZXFzdF92YWx1ZT0="
        self.userid="zzbocca"
        self.passwd="kaygugu88**"

    def __del__(self):
        super(Nanji, self).__del__()
        if hasattr(Nanji, 'my_d'):
            self.my_d.temDriver()

    def set_sel_site(self, str):
        dprint(str)
        self.sel_site = str

    def set_Telegram(self, tel):
        super(Nanji, self).set_Telegram(tel)
        self.add_cmd('nj', self.nanji_tel_set, "show nanji's settings")
        self.tel.add_cb_handler(self.nanji_tel_set_callback)

    def check_valid_time(self):
        now = super(Nanji, self).check_valid_time()
        if now is not None:
            self.now = now
            if now.day != self.now.day:
                if self.update_data() == 1:
                    self.get_reserve_url()
        else:
            self.now = None

        return self.now

    def login_nanji_with_execute_script(self, userid, userpw):
        self.driver.find_element_by_id("userid").send_keys(userid)
        self.driver.find_element_by_id("userpwd").send_keys(userpw)

        self.driver.find_element_by_xpath('//*[@id="addUserForm"]/div[1]/button').click()

    @staticmethod
    def search_url_parse(url):
        dprint(url, 5)
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

    def do_enable(self):
        self.clear_url_list()
        if self.update_data() == 1:
            self.get_reserve_url()

    def do_disable(self):
        self.update_data()

    # date update (remove past date and remove past reservation url)
    def update_data(self, from_file=0, date=1):
        diff = 0
        update = 0
        self.get_now_month()
        if from_file == 1:
            self.site_data.load_data()
            for mon in self.month_list:
                for site_name in self.nanji_site_name:
                    url_key = str(mon) + "월%20" + str(site_name)
                    if self.site_dict.get(url_key) is None:
                        self.site_dict[url_key] = ["", {}]
                        diff = 1

            dprint(self.site_dict, 11)

        if date == 1:
            dprint(self.site_dict, 9)
            delete_list = []
            delete_date = []
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
                        delete_list.append(key)
                        diff = 1
                        update = 1
                    else:
                        if len(value[1]) != 0:
                            for date in value[1].keys():
                                if int(date) < self.now_date:
                                    delete_date.append(date)
                                    diff = 1

                        for date in delete_date:
                            del value[1][date]
                            update = 1

                        delete_date.clear()
            for key in delete_list:
                del self.site_dict[key]

            delete_list.clear()
        else:
            update = 1

        if diff == 1:
            self.site_data.save_data()

        if update == 1:
            self.clear_url_list()
            return 1

        return 0

    # get reservation url
    def get_reserve_url(self):
        diff = 0
        if self.timeout == 0:
            return

        for key, value in self.site_dict.items():
            if len(value[0]) == 0:
                url = self.search_url_1+key+self.search_url_2
                value[0] = self.search_url_parse(url)
                diff = 1

            if len(value[1]) != 0:
                url = self.reserv_url_1+value[0]+self.reserv_url_2
                self.set_url(url)

        if diff == 1:
            self.site_data.save_data()
        dprint(self.url_list, 1)

    def get_available_value(self, count_str):
        if len(count_str) == 0:
            return 0
        elif count_str[2] == '/':
            remine = count_str[0:2]
            total = count_str[3:5]
        else:
            remine = count_str[0]
            if len(count_str) > 3 and count_str[3] == ')':
                total = count_str[2]
            else:
                total = count_str[2:]
        return int(total) - int(remine)

    # real parse data for reservation
    def parse_data(self, url=""):
        dprint(url, 2)
        self.ret_list.clear()

        with requests.Session() as s:
            self.driver.get(url)
            title = self.driver.find_element_by_xpath('//*[@id="aform"]/div[1]/h4/span[1]').text
            dprint(self.site_dict, 10)

            for key, value in self.site_dict.items():
                if key[2] == '%':
                    key_first = key[0:2]
                    key_sec = key[5:]
                else:
                    key_first = key[0:3]
                    key_sec = key[6:]

                if title.find(key_first) != -1 and title.find(key_sec) != -1:
                    check_day_night = 0
                    flag_day_night = 0
                    if key_sec.find("바비큐존")  != -1:
                        check_day_night = 1
                    for date, date_value in value[1].items():
                        id_str = "div_cal_" + date
                        if check_day_night:
                            flag_day_night = date_value[1]

                        dprint("id_str = " + id_str, 4)
                        data = self.driver.find_element_by_id(id_str)
                        dprint(str(date) + " reserved : " + data.text)
                        avail_value = self.get_available_value(data.text)
                        if avail_value != 0:
                            if flag_day_night > 0:
                                self.driver.get(self.login_url)
                                self.login_nanji_with_execute_script(self.userid, self.passwd)
                                booking_url = self.booking_url_1 + value[0] + self.booking_url_2 + date
                                self.driver.get(booking_url)
                                ret = self.driver.find_element_by_id("calendar_tm_area")
                                if ret is not None:
                                    index_start = 13
                                    if flag_day_night & SEL_DAY:
                                        day_index = ret.text.find("11:00")
                                        if day_index != -1:
                                            avail_value = self.get_available_value(ret.text[day_index+index_start:])
                                            result = key + " " + str(date) + "DAY 잔여수량 : " + str(avail_value) + " : " + url
                                            self.ret_list.append(result)
                                    if flag_day_night & SEL_NIGHT:
                                        night_index = ret.text.find("15:00")
                                        if night_index != -1:
                                            avail_value = self.get_available_value(ret.text[night_index+index_start:])
                                            result = key + " " + str(date) + "NIGHT 잔여수량 : " + str(avail_value) + " : " + url
                                            self.ret_list.append(result)
                            else:
                                result = key + " " + str(date) + " 잔여수량 : " + str(avail_value) + " : " + url
                                self.ret_list.append(result)

    # telegram cmd and callback
    def help(self, update, context):
        msg = 'Nanji help\n   - CMD List -\n'
        msg = msg + " /nj  : set reservation\n"
        msg = msg + "   - Status -\n"
        for site, value in self.site_dict.items():
            if len(value[1]) != 0:
                if site[5] == '0':
                    name = site[6:]
                else:
                    name = site[5:]
                msg = msg + "     +  " + name + "\n"
                for date, data in value[1].items():
                    msg = msg + "        -  " + date
                    if data[1] == 1:
                        msg += " Day"
                    elif data[1] == 2:
                        msg += " Night"
                    elif data[1] == 3:
                        msg += " All Day"
                    msg += "\n"

        self.tel.send_answer(msg)

    def nanji_get_rev_date(self, site_name):
        date_str = ""
        for mon in self.month_list:
            url_key = str(mon) + "월%20" + str(site_name)
            if self.site_dict.get(url_key) is not None:
                for date in self.site_dict[url_key][1].keys():
                    rev_date = date[4:6] + "/" + date[6:]
                    if len(date_str):
                        date_str += ", "
                    date_str += rev_date
        if len(date_str) == 0:
            date_str = "-"
        return date_str

    def nanji_send_site_list(self, first):
        group = list()
        for site in self.nanji_site_name:
            cb_data = self.tel_key_site + str(site)
            group.append([InlineKeyboardButton(text=site, callback_data=cb_data),
                          InlineKeyboardButton(text=self.nanji_get_rev_date(site), callback_data=cb_data)])
        group.append([InlineKeyboardButton(text="Exit", callback_data=self.tel_key_exit)])
        show_markup = InlineKeyboardMarkup(group)

        if first == 1:
            self.show_msg_id = self.tel.send_answer(f"Select site", show_markup=show_markup)
        else:
            self.show_msg_id = self.tel.send_answer(f"Select site", msg_id =self.show_msg_id, show_markup=show_markup)

    def nanji_send_day_night_list(self, day_night):
        group = list()
        if day_night & SEL_DAY :
            day_text = "(DAY)"
        else:
            day_text = "DAY"
        if day_night & SEL_NIGHT :
            night_text = "(Night)"
        else:
            night_text = "Night"
        group.append([InlineKeyboardButton(text=day_text, callback_data=self.tel_key_day_night + "1"),
                      InlineKeyboardButton(text=night_text, callback_data=self.tel_key_day_night + "2")])
        group.append([InlineKeyboardButton(text="Back", callback_data=self.tel_key_sel_cal),
                      InlineKeyboardButton(text="Exit", callback_data=self.tel_key_exit)])
        show_markup = InlineKeyboardMarkup(group)

        self.show_msg_id = self.tel.send_answer(f"Select Day or Night " + self.sel_date, msg_id =self.show_msg_id, show_markup=show_markup)

    def nanji_tel_set(self, update, context):
        self.send_msg = ""
        self.nanji_send_site_list(1)

    def nanji_get_disp_index(self, cb_str, msg_id):
        disp_cal = DISPLAY_NONE

        if cb_str.find(self.tel_key_site) != -1:
            disp_cal = DISPLAY_SITE
        elif cb_str.find(self.tel_key_date) != -1:
            disp_cal = DISPLAY_DATE
        elif cb_str.find(self.tel_key_day_night) != -1:
            disp_cal = DISPLAY_DN
        elif cb_str.find(self.tel_key_exit) != -1:
            self.tel.send_answer(self.send_msg, msg_id=msg_id)
        elif cb_str.find(self.tel_key_sel_site) != -1:
            self.nanji_send_site_list(0)
        elif cb_str.find(self.tel_key_sel_cal) != -1:
            if len(self.last_dn_date_key) > 0:
                disp_cal = DISPLAY_SITE

        return disp_cal

    def nanji_tel_set_callback(self, update, context):
        sel_day_night = SEL_NONE
        exist_day_night = 0
        cb = update.callback_query

        if cb.message.message_id != self.show_msg_id:
            return

        if isinstance(cb.data, str):
            cb_str = cb.data
            disp_cal = self.nanji_get_disp_index(cb_str, cb.message.message_id)

            if self.sel_site.find("바비큐존") != -1: # set exist_day_night all for  바베큐존
                exist_day_night = 1

            if disp_cal == DISPLAY_NONE:
                return
            elif disp_cal == DISPLAY_SITE:
                if len(self.last_dn_date_key) != 0:
                    cb_str = CAL_FIRST_STR + self.last_dn_date_key[12:]
                    dprint(cb_str)
                    self.last_dn_date_key = ""
                    site_month = self.sel_month
                else:
                    self.set_sel_site(cb_str[5:])
                    cb_str = CAL_FIRST_STR + str(self.now.year) + "_" + str(self.now.month) + "_" + str(self.now.day)
                    dprint(cb_str)
                    site_month = self.now.month
            elif disp_cal == DISPLAY_DATE:
                if cb_str[18] == '_':
                    site_month = int(cb_str[17:18])
                else:
                    site_month = int(cb_str[17:19])
            elif disp_cal == DISPLAY_DN:
                sel_day_night = int(cb_str[len(self.tel_key_day_night):])
                site_key = str(self.sel_month) + "월%20" + self.sel_site
                date_dict = self.site_dict[site_key][1]
                dprint(sel_day_night)
                if sel_day_night == SEL_DAY:
                    day_str = "day"
                elif sel_day_night == SEL_NIGHT:
                    day_str = "night"
                else:
                    day_str = ""
                    sel_day_night = SEL_NONE
                dprint(date_dict)
                if len(date_dict) != 0 and self.sel_date in date_dict:
                    if date_dict[self.sel_date][1] == SEL_ALL:
                        add_del = DATE_DEL
                        date_dict[self.sel_date][1] &= ~sel_day_night
                    elif date_dict[self.sel_date][1] == sel_day_night:
                        add_del = DATE_DEL
                        del date_dict[self.sel_date]
                    else:
                        date_dict[self.sel_date][1] |= sel_day_night
                        add_del = DATE_ADD
                else:
                    date_dict[self.sel_date] = [0, sel_day_night]
                    add_del = DATE_ADD

                if add_del == DATE_DEL:
                    self.send_msg += f"{self.sel_site}'s {self.sel_date} {day_str} is canceled reservation." + os.linesep
                else:
                    self.send_msg += f"{self.sel_site}'s {self.sel_date} {day_str} is reservated." + os.linesep

                if self.update_data(0, 0) == 1:
                    self.get_reserve_url()
                self.site_data.save_data()
                return

            result, key, step = DetailedTelegramCalendar().process(cb_str)
            if not result and key:
                if isinstance(key, tuple):
                    value = key[1]
                else:
                    value = key

                key_dict = json.loads(value)

                key_list = list(key_dict.values())
                first_sunday = key_list[0][1][6]['text']
                first_date = 7 - first_sunday

                site_key = str(site_month) + "월%20" + self.sel_site

                if self.site_dict.get(site_key):
                    for date, value in self.site_dict[site_key][1].items():
                        day = int(date) % 100
                        cal_day = day + first_date - 1
                        col = 1 + (cal_day // 7)
                        row = cal_day % 7

                        if sel_day_night == SEL_NONE:
                            sel_day_night = value[1]

                        if sel_day_night == SEL_NONE or sel_day_night == SEL_ALL:
                            key_list[0][col][row]['text'] = f"({day})"
                        elif sel_day_night == SEL_DAY:
                            key_list[0][col][row]['text'] = f"({day}"
                        elif sel_day_night == SEL_NIGHT:
                            key_list[0][col][row]['text'] = f"{day})"

                add_col = len(key_list[0]) - 2
                key_list[0][add_col].append({'text': "Back", 'callback_data': self.tel_key_sel_site})
                key_list[0][add_col].append({'text': "Exit", 'callback_data': self.tel_key_exit})

                dprint(key_dict, 11)
                self.tel.send_answer(f"[{self.sel_site}]의 날짜를 선택하세요! ( 오늘 : {self.now_date} )",
                                        msg_id=cb.message.message_id, show_markup=key_dict)
            elif result:
                result_date = str(result.year * 10000 + result.month * 100 + result.day)
                dprint(self.sel_site)
                site_key = str(result.month) + "월%20" + self.sel_site
                date_dict = self.site_dict[site_key][1]
                if len(date_dict) != 0 and result_date in date_dict:
                    add_del = 2
                    dn_value = date_dict[result_date][1]
                else:
                    add_del = 1
                    dn_value = 0

                if exist_day_night == 1:
                    self.sel_date = result_date
                    self.sel_month = result.month
                    self.last_dn_date_key = cb_str
                    self.nanji_send_day_night_list(dn_value)
                    return
                else:
                    if add_del == 2:
                        self.send_msg += f"{self.sel_site}'s {result_date} is canceled reservation." + os.linesep
                    elif add_del == 1:
                        self.send_msg += f"{self.sel_site}'s {result_date} is reservated." + os.linesep

                if add_del == 1:
                    date_dict[result_date] = [0, 0]
                elif add_del == 2:
                    del date_dict[result_date]

                if self.update_data(0, 0) == 1:
                    self.get_reserve_url()
                self.site_data.save_data()
