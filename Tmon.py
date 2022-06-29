
import os.path
from bs4 import BeautifulSoup
import requests
from lib.MyDebug import Dprint as dprint
from lib import MyParser
from lib import MyBdriver

class Tmon(MyParser.MyParser):
    def __init__(self, timeout):
        super(Tmon, self).__init__(timeout, send_to_ch=2, disable_preview='False')
        self.set_url("http://www.tmon.co.kr/planning/PLAN_HdFdhvWIZx")
        self.my_d = MyBdriver.myBdriver()
        self.driver = self.my_d.getDriver()

    def __del__(self):
        super().__del__()

    def parse_data(self, url):
        with requests.Session() as s:
            self.driver.get(url)
            #print(self.driver.page_source)

            ret = self.driver.find_elements_by_class_name('anchor')
            for item in ret:
                if len(item.text):
                    start_index = item.text.find('[10분어택]')
                    end_index = item.text.find('오늘만 선물하기')
                    if start_index != -1 and item.text.find('판매종료') == -1:
                        ref = item.get_attribute('href')
                        if end_index > 0:
                            ret_data = item.text[start_index:end_index] + " " + ref
                        else:
                            ret_data = item.text[start_index:] + " " + ref
                        print(ret_data)
                        self.ret_list.append(ret_data)

        self.set_sch_timeout(86400)