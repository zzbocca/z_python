import Nanji
import Sdeal
import Suanbo
from lib import MyDebug
from lib import MyTel
from lib import MyFile
import ChungDab
import Nanji
import Sdeal
import Suanbo
import datetime
import http.client


class MyProc:
    def __init__(self):
        self.wc_list = []

        self.tel = MyTel.MyTel()
        ChungDab.ChungDab()
        self.wc_list.append()
        self.wc_list.append(Nanji.Nanji())
        self.wc_list.append(Sdeal.SDeal())
        self.wc_list.append(Suanbo.Suanbo())

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    MyDebug.Denable(1)
    MyDebug.Dprint('PyCharm')

    proc = ChungDab.ChungDab()
    tel = MyTel.MyTel()
    proc.parse_start(tel)