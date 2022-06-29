
import os.path
from bs4 import BeautifulSoup
import requests
from lib import MyDebug
from lib import MyTel
from lib import MyParser


class Sdeal(MyParser.MyParser):
    def __init__(self, timeout):
        super(Sdeal, self).__init__(timeout, send_to_ch=2, disable_preview='False')
        self.set_url("https://deal.11st.co.kr/browsing/DealAction.tmall?method=getTimeDeal")

    def __del__(self):
        super().__del__()

    def parse_sdeal(self, soup):
        send_data = ""
        ret_data = []
        index = 2
        count = 0

        while count < 10:
            result = soup.select_one(
                "#layBody > div.md_wrap.sub_md > div:nth-child(" + str(index) + ") > div > div > div > a")
            MyDebug.Dprint(result, 8)
            if result is None:
                break
            url = result['href']
            MyDebug.Dprint(url, 8)

            result = soup.select_one(
                "#layBody > div.md_wrap.sub_md > div:nth-child(" + str(
                    index) + ") > div > div > div > a > div.prd_info > p")
            MyDebug.Dprint(result.text, 8)
            name = result.text

            result = soup.select_one(
                "#layBody > div.md_wrap.sub_md > div:nth-child(" + str(
                    index) + ") > div > div > div > a > div.prd_info > div.price_info > span.price_detail > strong")
            price = result.text

            MyDebug.Dprint(result.text, 8)
            index = index + 1
            count = count + 1

            send_data += name + " : " + price + os.linesep + url + os.linesep

        MyDebug.Dprint(send_data, 7)
        ret_data.append(send_data)
        send_data = ""

        index = 1
        count = 0

        while count < 200:
            result = soup.select_one(
                "#layBody > div.md_wrap.sub_md > div.list_view.list_time_deal > div > ul > li:nth-child(" + str(
                    index) + ") > div > a")
            if result is None:
                break
            MyDebug.Dprint(result.text, 8)
            num = result['name']
            open_time = result['onclick']
            only_time = open_time[7:21]
            MyDebug.Dprint(num + only_time, 8)
            result = soup.select_one(
                "#layBody > div.md_wrap.sub_md > div.list_view.list_time_deal > div > ul > li:nth-child(" + str(
                    index) + ") > div > a > div.prd_info > p")
            if result is None:
                break
            name = result.text
            MyDebug.Dprint(name, 8)

            url = "https://www.11st.co.kr/products/" + num + "?trTypeCd=48"
            send_data += " * " + only_time + " : " + name + os.linesep + url + os.linesep

            index = index + 1
            count = count + 1
            if count % 20 == 0:
                ret_data.append(send_data)
                send_data = ""

        if len(send_data) != 0:
            ret_data.append(send_data)

        if len(ret_data) != 0:
            self.ret_list.clear()
            self.ret_list.extend(ret_data)

    def parse_data(self, url):
        with requests.Session() as s:
            res = s.get(url)
            if res.status_code == requests.codes.ok:
                soup = BeautifulSoup(res.text, 'lxml')
                self.parse_sdeal(soup)

        self.set_sch_timeout(86400)


