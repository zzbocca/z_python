import sys
import importlib
from lib import MyDebug
from lib.MyData import MyDict
from lib.MyTel import MyTel
from lib.MySchd import MySchd
from lib import MyFile

data_enable = {"ChungDab": 0,
                  "Nanji": 60,
                  "Sdeal": 0,
                  "Suanbo": 0
                }
parser_obj_list = []

#pdata_filename = "./output/pdata.txt"

class MyProc:
    def str_to_class(self, module_name):
        module = __import__(module_name)
        class_ = getattr(module, module_name)
        return class_

    def parser_init(self):
        global data_enable
        for key, value in data_enable.items():
            class_=self.str_to_class(key)
            parser = class_(value)
            MyDebug.Dprint(type(parser))
            self.pdata.add_data(key, value)
            self.parser_list.append(parser)

    def enabled_data_add(self):
        self.parser_init()

    def __init__(self):
        self.pdata = MyDict()
        self.tel = MyTel()
        self.mySchd = MySchd(self.tel)
        self.parser_list = []
        if self.pdata.get_data_len() == 0:
            self.enabled_data_add()

        print(self.pdata.get_data())
        for parser in self.parser_list:
            print(parser)
            self.mySchd.add_schedule(parser)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    MyDebug.Denable(4)
    proc = MyProc()

