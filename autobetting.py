#coding=utf-8
import splinter
import time
import random
import requests
import re
import codecs
import hashlib
from bs4 import BeautifulSoup
from splinter import Browser
from selenium import webdriver
from pymongo import MongoClient

#http://docs.python-requests.org/en/latest/user/advanced/#session-objects
#http://zhaofei.tk/2014/09/03/how_to_crawl_coursera/

cart_url = "http://1.163.com/cart/index.do"
bonus_url = "http://1.163.com/user/bonus.do"
login_url = "https://reg.163.com/login.jsp"
logininfo = {"username": "", "password": "","product": "mail163","url":"http://1.163.com","savelogin":""}

user_agent = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) "
              "AppleWebKit/537.36 (KHTML, like Gecko) "
              "Chrome/36.0.1985.143 Safari/537.36")

post_headers = {"User-Agent": user_agent,"Referer": "http://1.163.com"}

class User(object):
    def __init__(self, email, passwd):
        super(User, self).__init__()
        self.email = email
        self.passwd = passwd
        logininfo['username'] = email
        logininfo['password'] = passwd
        
    def __unicode__(self):
        return self.email

    def login(self):
        self.login_session = requests.Session()
        login_res = self.login_session.post(login_url, data=logininfo,headers=post_headers,)
        print login_res.status_code
        if login_res.status_code == 200:
           return True
        else:
            return False
    def getbonus(self):
        login_res = self.login_session.get(bonus_url)
        print login_res.text
def main():
    user = User("xxx@163.com", "yyy")
    if user.login():
        user.getbonus()
if __name__ == '__main__':
    main()