#!/usr/bin/python3
# -*- coding: cp949 -*-

import re
import sys
import io
from telegram import Bot
#from telegram.ext import Dispatcher
#from threading import Thread
#from queue import Queue
from lib import MyDebug
from lib import MyData

class MyTel:
    def __init__(self):
        self.tel_data = MyData.MyDict("./data/my_token.txt")
        self.saving_tel_data()
        self.tel_data.load_data()
        self.send = 0
        if self.tel_data.get_data_len() == 0:
            MyDebug.Dprint("TOKEN Data do not exist.", 0)
        data = self.tel_data.get_data()
        self.mytoken = data['my_token']
        self.chat_id = data['my_chat_id']   #chatting id for only aykim
        self.chan_id = data['my_chan_id']   #channel id for all group
        self.setup()

    def saving_tel_data(self):
        self.tel_data.add_data("my_token", "1695159376:AAF1pmkgMneBm3dmiaG_w1oBjBpz55esCNc")
        self.tel_data.add_data("my_chat_id", '1681474946')
        self.tel_data.add_data("my_chan_id", '1681474946')
        self.tel_data.save_data()

    def setup(self):
        print(self.mytoken)
        self.bot = Bot(token=self.mytoken)
        #self.update_queue = Queue()
        #self.dispatcher = Dispatcher(self.bot, self.update_queue)
        #if self.thread :
        #    self.thread.stop()
        #    self.thread.delete()

        #self.thread = Thread(target = self.dispatcher.start, name = 'dispatcher')
        #self.thread.start()

    def disconnect(self):
        self.send = 0

    def set_token(self, m_token):
        self.mytoken = m_token

    def send_answer(self, value, to_chan = 0, msg_id = 0):
        MyDebug.Dprint(value, 1)

        if self.send == 0:
            return None

        if to_chan == 0:
            self.bot.sendMessage(chat_id=self.chat_id, text=value)
            return 0
        else:
            if msg_id is not None and msg_id != 0:
                self.bot.edit_message_text(chat_id=self.chan_id, text=value, message_id=msg_id)
                return msg_id
            else:
                return self.bot.sendMessage(chat_id=self.chan_id, text=value)['message_id']


    def webhook(self, update):
        pass
        #self.update_queue.put(update)

    async def newMessageListener(self, event):
        pass
        #newMessage = event.message.message

        #subjectFiltered = re.findall(r"()")