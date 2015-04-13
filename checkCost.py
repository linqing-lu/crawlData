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

base_url = "http://1.163.com/record/getDuobaoRecord.do?"
user_agent = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) "
              "AppleWebKit/537.36 (KHTML, like Gecko) "
              "Chrome/36.0.1985.143 Safari/537.36")

post_headers = {"User-Agent": user_agent,"Referer": "http://1.163.com"}
class Goods(object):
	def __init__(self, gid, period):
		super(Goods, self).__init__()
		self.gid = gid
		self.period = period
		self.session = requests.Session()
		url = str("http://1.163.com/detail/%02d-%02d-%02d-%02d-%02d.html") \
		% (gid/100, gid%100, period/10000, period%10000/100, period%100)
		print url
		r = self.session.get(url,headers=post_headers)
		if r.status_code == 200:
			cookie = r.headers['set-cookie']
			strs = cookie.split(';')
			otoken = strs[0]
			self.token = otoken.split('=')[1]
			print 'create session success'
		else:
			print 'create session failed'

	def checkCost(self):
		info = {'gid':self.gid,'period':self.period,'t':1428847870372,'token':self.token}
		info['pageSize'] = 250
		info['pageNum'] = 1
		info['totalCnt'] = 0
		res = self.session.get(base_url, params=info)
		if res.status_code == 200:
			result = res.json()
			result = result['result']
			print result['totalCnt']
			print result['pageSize']
			print result['pageNum']
			costlist = result['list']
			for cost in costlist:
				pass
def main():
	g = Goods(146, 344)
	g.checkCost()
if __name__ == '__main__':
	main()		