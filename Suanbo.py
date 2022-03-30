
from dateutil.relativedelta import relativedelta
import sys
import io
from bs4 import BeautifulSoup
import requests
import datetime
from lib import MyDebug
from lib import MyTel
from lib import MyParser

URL1="http://soohotel.netfuhosting.com/n_time/m/page/index.php?year=2022&month="
URL2="&day=01&group=20201016161347_6270"


class Suanbo(MyParser.MyParser):
    def __init__(self, timeout):
        super(Suanbo, self).__init__(timeout)
        self.month_list=[]
        self.search_url()

    def __del__(self):
        super().__del__()

    def parse_data(self, url):
        MyDebug.Dprint(url)
        self.ret = ""
        smessage = ""

        with requests.Session() as s:
            res = s.get(url)
            if res.status_code == requests.codes.ok:
                soup = BeautifulSoup(res.text, 'lxml')

                result = soup.find_all("a", class_="under hand num11")
                for block in result:
                    MyDebug.Dprint(block, 7)
                    ret = block.findChildren()
                    ch = ret[0]
                    MyDebug.Dprint(ch, 7)

                    if ch is not None and len(ch) != 0:
                        color = ch['class'][0]
                        print(color)
                        day = ch.text

                        if color == "blue":
                            smessage = smessage + "예약 가능 : " + str(day) + " " + url + "\n"

        if len(smessage) > 0:
            self.ret = smessage

    def search_url(self):
        check_next_month=0
        now=datetime.datetime.today()
        after_month=now + relativedelta(months=1)

        if after_month.day < 7 and after_month.isoweekday() < 6:
            if after_month.day - after_month.isoweekday() > 0:
                check_next_month = 1
        else:
            check_next_month = 1

        self.month_list.append(now.month)
        if check_next_month == 1:
            self.month_list.append(after_month.month)

        for mon in self.month_list:
            url = URL1 + str(mon) + URL2
            self.set_url(url)

