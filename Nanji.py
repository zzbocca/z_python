import schedule
import time
import sys
import io
from bs4 import BeautifulSoup
import requests
import telegram
import datetime
import pytz
from selenium import webdriver
import webbrowser
from inspect import currentframe
from apscheduler.schedulers.blocking import BlockingScheduler
from lib import MyBdriver

class Nanji:
    def __init__(self):
        self.driver = MyBdriver()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.temDriver()

