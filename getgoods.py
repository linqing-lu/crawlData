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

base_url = "http://1.163.com/goods/getPeriod.do?"
user_agent = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) "
              "AppleWebKit/537.36 (KHTML, like Gecko) "
              "Chrome/36.0.1985.143 Safari/537.36")

post_headers = {"User-Agent": user_agent,"Referer": "http://1.163.com"}
class GoodsInfo(object):
	"""docstring for GoodsInfo"""
	def __init__(self, goods_id):
		super(GoodsInfo, self).__init__()
		self.goods_id = goods_id
		self.dbclient = MongoClient('mongodb://198.52.117.75', 27017)
		self.db = self.dbclient.duobao
		self.db.authenticate('test', 'duobao')
	def __unicode__(self):
		return self.goods_id
	def fetchOne(self, period):
		session = requests.Session()
		r = session.get('http://1.163.com',headers=post_headers)
		if r.status_code == 200:
			cookie = r.headers['set-cookie']
			strs = cookie.split(';')
			otoken = strs[0]
			token = otoken.split('=')[1]
			info = {'gid':self.goods_id,'period':period,'t':1428847870372,'token':token}
			res = session.get(base_url, params=info)
			if res.status_code == 200:
				result = res.json()
				result = result['result']['periodWinner']
				detail = {}
				m = hashlib.md5()
				m.update(result['goods']['gname'].encode('utf8'))
				detail['_id'] = str("%s_%d") % (m.hexdigest(), period)
				detail['title'] = result['goods']['gname']
				detail['price'] = result['goods']['price']
				detail['issue'] = period
				detail['cost'] = result['ownerCost']
				detail['winner_cid'] = result['owner']['cid']
				detail['winner_uid'] = result['owner']['uid']
				detail['ip_address'] = result['owner']['IPAddress']
				detail['lucky_code'] = result['luckyCode']
				print period
				self.saveToMongoDB(detail, self.db.detail)
			else:
				print res.status_code
	def saveToMongoDB(self, data, collection):
		collection.save(data);
def main():
	g = GoodsInfo(158)
	for i in range(1, 3000):
		g.fetchOne(i)
if __name__ == '__main__':
	main()