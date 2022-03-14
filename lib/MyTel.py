import re
import sys
import io
from telegram import Bot
#from telegram.ext import Dispatcher
#from threading import Thread
#from queue import Queue
from lib import MyDebug

class MyTel:
    def __init__(self):
        self.mytoken = '1695159376:AAF1pmkgMneBm3dmiaG_w1oBjBpz55esCNc'
        self.chat_id = '1681474946'
        self.send = 1
        self.setup()

    def setup(self):
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

    def send_answer(self, value, msg_id):
        MyDebug.Dprint(value)

        if self.send == 0:
            return None

        if msg_id is not None:
            self.bot.edit_message_text(chat_id=self.chat_id, text=value, message_id=msg_id)
            return msg_id
        else:
            return self.bot.sendMessage(chat_id=self.chat_id, text=value)['message_id']


    def webhook(self, update):
        pass
        #self.update_queue.put(update)

    async def newMessageListener(self, event):
        pass
        #newMessage = event.message.message

        #subjectFiltered = re.findall(r"()")