#!/usr/bin/python3
# -*- coding: cp949 -*-

from telegram import Bot
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from lib.MyDebug import Dprint as dprint

#import telebot
from lib import MyDebug
from lib import MyData

class MyTel:
    def __init__(self):
        self.tel_data = MyData.MyDict("./data/my_token.txt")
        self.tel_data.load_data()
        self.send = 1
        if self.tel_data.get_data_len() == 0:
            dprint("TOKEN Data do not exist.", 0)
        data = self.tel_data.get_data()
        self.mytoken = data['my_token']
        self.chat_id = data['my_chat_id']   #chatting id for only aykim
        self.chan_list = []
        for key, value in data.items():
            if key[:10] == 'my_chan_id':
                self.chan_list.append(value)

        self.bot = Bot(self.mytoken)
        self.updater = Updater(self.mytoken)

    def __del__(self):
        self.updater.dispatcher.stop()
        self.updater.job_queue.stop()
        self.updater.stop()

    def disconnect(self):
        self.send = 0

    def send_answer(self, value, to_chan=0, msg_id=0, show_markup=None):
        dprint(value, 1)

        if self.send == 0:
            return None
        if to_chan == 0:
            id = self.chat_id
        elif to_chan > 0:
            index = to_chan - 1
            id = self.chan_list[index]
        dprint(id, 1)

        if show_markup is not None:
            if msg_id is not None and msg_id != 0:
                return self.bot.edit_message_text(chat_id=id, text=value, message_id=msg_id,
                                           reply_markup=show_markup)['message_id']
            else:
                return self.bot.sendMessage(chat_id=id, text=value, reply_markup=show_markup)['message_id']
        else:
            if to_chan == 0:
                self.bot.sendMessage(chat_id=id, text=value, parse_mode="HTML", disable_web_page_preview="true")#, parse_mode="Markdown")
                return 0
            else:
                if msg_id is not None and msg_id != 0:
                    return self.bot.edit_message_text(chat_id=id, text=value, message_id=msg_id, parse_mode="HTML", disable_web_page_preview="true")['message_id']
                else:
                    return self.bot.sendMessage(chat_id=id, text=value, parse_mode="HTML", disable_web_page_preview="true")['message_id']

    def add_handler(self, cmd, func):
        self.updater.dispatcher.add_handler(CommandHandler(cmd, func))

    def add_cb_handler(self, func):
        self.updater.dispatcher.add_handler(CallbackQueryHandler(func))

    def poll(self):
        self.updater.start_polling()
        self.updater.idle()

