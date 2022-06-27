from copy import deepcopy
from lib import MyDebug
from lib.MyDebug import Dprint as dprint
from lib.MyData import MyDict
from lib.MyTel import MyTel
from lib.MySchd import MySchd
from ast import literal_eval
import re

parser_obj_list = []

main_filename = "./data/main.txt"


class MyProc:
    def __init__(self):
        self.pdata = MyDict(main_filename)
        self.pdata.load_data()
        self.parser_obj = MyDict()
        self.tel = MyTel()
        self.mySchd = MySchd(self.tel)
        self.parser = {}
        if len(self.pdata.dic_data) == 0:
            self.parser_list = {
                'c': ["ChungDab", 0],
                'p': ["Naverpay", 3600],
                'n': ["Nanji", 0],
                'd': ["Sdeal", 0],
                's': ["Suanbo", 0]
            }
            self.pdata.save_data(self.parser_list)
        else:
            self.parser_list = deepcopy(self.pdata.dic_data)

        self.parser_init()

        for key, value in self.parser_obj.dic_data.items():
            if value is not None:
                value.set_Telegram(self.tel)
                value.schd_event = self.mySchd.add_schedule(value)
                if value.schd_event is None:
                    self.parser_list[key][1] = 0

        self.pdata.save_data(self.parser_list)

        self.tel.add_handler('h', self.help)
        self.tel.add_handler('s', self.set_timeout_from_bot)

    @staticmethod
    def str_to_class(module_name):
        module = __import__(module_name)
        class_ = getattr(module, module_name)
        return class_

    @staticmethod
    def str_diff_parse(diff):
        return [tuple(literal_eval(y) for y in re.findall(r"\[('?\w+'?)\]", diff))]

    def parser_init(self):
        for key, value in self.parser_list.items():
            class_ = self.str_to_class(value[0])
            self.parser_obj.add_data(key, class_(value[1]))

    def help(self, update, context):
        msg = "Aykim's Telegram\n"    \
                "\t-  Now Status and CMD -  \n"
        if len(context.args) == 0:
            modules = ""
            for key, value in self.pdata.dic_data.items():
                msg = msg + "/s " + key + " [timeout]  : set the " + value[0] + "'s timeout. now = (" + str(value[1]) + " sec)\n"
                modules = modules + key + " "

            msg = msg + "\n/h [" + modules + "] : print module's help"
            self.tel.send_answer(msg)
        else:
            cmd = context.args[0]
            self.parser_obj.dic_data[cmd].help(update, context)

    def set_timeout_from_bot(self, update, context):
        if len(context.args) != 0:
            cmd = context.args[0]
            timeout = int(context.args[1])
            self.parser_list[cmd][1] = timeout
            self.parser_obj.dic_data[cmd].set_sch_timeout(timeout)

            diff = self.pdata.get_diff_data(self.parser_list)
            updated = diff['values_changed']
            for key, value in updated.items():
                list_index = self.str_diff_parse(key)
                for index in list_index:
                    if index[1] == 1:
                        parser = self.parser_obj.dic_data[index[0]]
                        new_v = value['new_value']
                        dprint(new_v)
                        parser.set_sch_timeout(new_v)
                        if new_v == 0 and parser.schd_event is not None:
                            self.mySchd.del_schedule(parser.schd_event)
                            parser.schd_event = None
                        elif new_v != 0:
                            if parser.schd_event is not None:
                                self.mySchd.del_schedule(parser.schd_event)
                            parser.schd_event = self.mySchd.add_schedule(parser)
                            dprint(parser.schd_event)
                            if parser.schd_event is None:
                                self.parser_list[index[0]][1] = 0

            if len(updated):
                self.pdata.save_data(self.parser_list)

    def set_timeout_parser(self, update, context):
        pass
        #context.args[0]


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    MyDebug.Denable(0)
    proc = MyProc()
    proc.tel.poll()
