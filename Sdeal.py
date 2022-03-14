
import os.path
from bs4 import BeautifulSoup
import requests
from lib import MyDebug
from lib import MyTel
from lib import MyParser

class SDeal(MyParser):
    def __init__(self):
        super.__init__("https://deal.11st.co.kr/browsing/DealAction.tmall?method=getTimeDeal")

    def __exit__(self, exc_type, exc_val, exc_tb):
        super().__exit__()

    def parse_data(self, url):
        send_data = ""
        ret_data = []

        with requests.Session() as s:
            res = s.get(url)
            if res.status_code == requests.codes.ok:
                soup = BeautifulSoup(res.text, 'lxml')
                index = 2
                count = 0
                while count < 10:
                    result = soup.select_one("#layBody > div.md_wrap.sub_md > div:nth-child(" + str(index) + ") > div > div > div > a")
                    MyDebug.Dprint(result)
                    if result is None :
                        break
                    url = result['href']
                    MyDebug.Dprint(url)

                    result = soup.select_one(
                        "#layBody > div.md_wrap.sub_md > div:nth-child(" + str(index) + ") > div > div > div > a > div.prd_info > p")
                    MyDebug.Dprint(result.text)
                    name = result.text

                    result = soup.select_one(
                        "#layBody > div.md_wrap.sub_md > div:nth-child(" + str(index) + ") > div > div > div > a > div.prd_info > div.price_info > span.price_detail > strong")
                    price = result.text

                    MyDebug.Dprint(result.text)
                    index = index + 1
                    count = count + 1

                    send_data += name + " : " + price + os.linesep + url +os.linesep
                    continue
                ret_data.append(send_data)
                send_data = ""

                index = 1
                count = 0

                while count < 200:
                    result = soup.select_one(
                        "#layBody > div.md_wrap.sub_md > div.list_view.list_time_deal > div > ul > li:nth-child(" + str(index) + ") > div > a")
                    if result is not None:
                        break
                    MyDebug.Dprint(result.text)
                    num = result['name']
                    open_time = result['onclick']
                    only_time = open_time[7:21]
                    MyDebug.Dprint(num + only_time)
                    result = soup.select_one(
                        "#layBody > div.md_wrap.sub_md > div.list_view.list_time_deal > div > ul > li:nth-child(" + str(index) + ") > div > a > div.prd_info > p")
                    if result is not None:
                        break
                    name = result.text
                    MyDebug.Dprint(name)

                    url = "https://www.11st.co.kr/products/"+ num + "?trTypeCd=48"
                    send_data += " * " + only_time + " : " + name + os.linesep + url + os.linesep

                    index = index + 1
                    count = count + 1
                    if count % 25 == 0 :
                        ret_data.append(send_data)
                        send_data = ""
                ret_data.append(send_data)

        return ret_data