
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

class Suanbo(MyParser):
    def __init__(self):
        super(Suanbo, self).__init__()
        self.month_list=[]

    def __exit__(self, exc_type, exc_val, exc_tb):
        super().__exit__()

    def parse_data(self ,url):
        ret_list = []
        with requests.Session() as s:
            res = s.get(url)
            if res.status_code == requests.codes.ok:
                soup = BeautifulSoup(res.text, 'lxml')

                result = soup.find_all("td", class_="td03")
                for tds in result:
                    classn = tds["class"]

                    if len(classn) >=2 :
                        if classn[1] == "bg_org" or classn[1] == "bg_gre":
                            continue

                    MyDebug.Dprint(classn)
                    colors = tds.font["class"]
                    day = tds.font.text

                    MyDebug.Dprint(colors)
                    if colors[0] == "dgr":
                        continue

                    for color in colors:
                        if color == "blue":
                            smessage = "예약 가능 : " str(day) + " " + base_url
                            ret_list.append(smessage)
        return ret_list

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

