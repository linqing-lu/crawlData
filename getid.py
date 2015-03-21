#coding=utf-8
import splinter
import time
import random
import requests
import re
import codecs
from bs4 import BeautifulSoup
from splinter import Browser
from selenium import webdriver
from pymongo import MongoClient
cid = 31768998
class Fetcher(object):
	urls = []
	dbclient = 0;
	local_db_client = 0;
	local_db = 0;
	db = 0;
	sqlite_db = 0;
	def __init__(self, arg):
		super(Fetcher, self).__init__()
		self.arg = arg
		self.dbclient = MongoClient('mongodb://198.52.117.75', 27017)
		self.db = self.dbclient.duobao
		self.db.authenticate('test', 'duobao')
		self.local_db_client = MongoClient('mongodb://localhost', 27017)
		self.local_db = self.local_db_client.duobao

	def fetchUrl(self, url):
		# url = str(self.baseurl) % (cid)
		# self.urls.append(url)
		save_data = {"_id": url, 'visited': 1}
		self.saveToMongoDB(save_data, self.local_db.urls)

		res = requests.get(url)
		html = res.content
		try:
			html = html.decode('utf-8')
		except:
			pass
		soup = BeautifulSoup(html, "lxml")
		# print(soup.prettify())
		# print(soup.find_all('a'))
		links = soup.find_all('a', href=re.compile('http://1.163.com/user/index.do'))
		for link in links:
			addr = link.get('href').strip()
			if self.checkUrl(addr):
				pass
			else:
				print(str('---------------------fetchurl:') + addr)
				# self.urls.append(addr)
				self.fetchUrl(addr)

	def checkUrl(self, url):
		# for turl in self.urls:
		# 	if turl == url:
		# 		return True
		# return False
		if self.local_db.urls.find({"_id": url}).count() > 0:
			return True
		else:
			self.fetchCID(url)
			save_data = {"_id": url, 'visited': 1}
			self.saveToMongoDB(save_data, self.local_db.urls)
			return False
	#从URL中提取cid
	def fetchCID(self, url):
		SEARCH_PAT = re.compile(r'cid\s*=\s*(\d+)')
		src_line = url
		pat_search = SEARCH_PAT.search(src_line)
		if pat_search != None:
			cid = pat_search.group(1)
			print cid
			id_data = {"_id": cid, "searched": 0}
			self.saveToMongoDB(id_data, self.db.users)
	def saveToMongoDB(self, data, collection):
		collection.save(data)

	def uninit(self):
		self.db.logout()
		self.dbclient.close()
		self.local_db.logout()
		self.local_db_client.close()
		
	def __unicode__(self):
		return self.dbclient
def main():
	fetcher = Fetcher(0)
	fetcher.fetchUrl('http://1.163.com')
	fetcher.uninit()
if __name__ == '__main__':
	main()
