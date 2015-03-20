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
cid = 20592113
class Duobao:
	filter1 = "\?cid="
	filter2 = "index.do\?cid="
	filter3 = "win.do\?cid="
	baseurl = "http://1.163.com/user/index.do?cid=%d"
	winurl = "http://1.163.com/user/win.do?cid=%d"
	urls = []
	total_count = 0
	def getdata(self):
		url = str(self.baseurl) % (cid)
		res = requests.get(url)
		html = res.content
		try:
			html = html.decode('utf-8')
		except:
			pass
		# print(html)
		soup = BeautifulSoup(html, "lxml")
		# print(soup.prettify())
		# print(soup.find_all('a'))
		links = soup.find_all('a', href=re.compile(self.filter1))
		for link in links:
			addr = link.get('href')
			if self.checkUrl(addr):
				pass
			else:
				print(str('---------------------geturl:') + addr)
				# self.getdatas(addr)
				self.urls.append(addr)
				self.getdatas(addr)
			
			# print(addr)
	def getdatas(self, url):
		self.crawData(url, 'code')
		res = requests.get(url)
		html = res.content
		try:
			html = html.decode('utf-8')
		except:
			pass
		# print(html)
		soup = BeautifulSoup(html, "lxml")
		# print(soup.prettify())
		# print(soup.find_all('a'))
		links = soup.find_all('a', href=re.compile(self.filter2))
		for link in links:
			addr = link.get('href')
			if self.checkUrl(addr):
				print('url exists!')
				pass
			else:
				print(str('---------------------geturl:') + addr)
				self.urls.append(addr)
				self.getdatas(addr)
			
	def checkUrl(self, url):
		# print self.urls
		# print url
		for turl in self.urls:
			if turl == url:
				return True
		return False
	def browseUrl(self, url):
		with Browser('chrome') as browser:
			browser.visit(url)
			sp = BeautifulSoup(browser.html, "lxml")
			print(sp.prettify())

	def crawData(self, url, tag_name):
		self.total_count = 0
		driver = webdriver.PhantomJS()
		driver.get(url);
		running = True
		fp = codecs.open("/Users/lm/test.txt", 'a+', 'utf-8')
		data = driver.find_elements_by_tag_name('table')
		while running:
			self.dealData(data, fp)
			running = len(data) > 10
			print running
			if running:
				btn_next = driver.find_element_by_class_name('w-pager-next')
				btn_next.click()
				time.sleep(1)
				data = driver.find_elements_by_tag_name('table')
		fp.close()
		driver.quit()
		save_data = {"cid": cid, "total_count": self.total_count}
		self.saveToMongoDB(save_data)

	def dealData(self, data, fp):
		for dt in data:
			print dt.text
			total_price = 0
			winner_price = 0
			try:
				col4 = dt.find_element_by_class_name('col4')
				print col4.text
				prices = re.findall(r'(\w*[0-9]+)\w*', col4.text)
				print prices
				self.total_count = self.total_count + int(prices[0])
			except Exception, e:
				pass

			try:
				winner = dt.find_element_by_class_name('winner')
				# print winner.text
				winner_name = winner.find_element_by_class_name('name')
				# print winner_name.text
				winner_vote = winner_name.find_element_by_class_name('txt-dark')
				winner_price = winner_vote.text
				print winner_price	#
			except Exception, e:
				pass

			try:
				goods_price = dt.find_element_by_class_name('w-goods-price')
				print goods_price.text
				total_price = re.findall(r'(\w*[0-9]+)\w*', goods_price.text)
			except Exception, e:
				print 'Exception raise'
			else:
				pass
			if total_price != 0:
				print str("%s/%s") % (winner_price, total_price[0])
			# temp = dt.text.decode('utf8')
			# m = re.findall(r'(\w*[0-9]+)(\W*[/u4e00-/u9fa5]+)\w*', temp)
			# print m
			# fp.write(dt.text);
			# fp.write("\n=====================================\n")
			print "====================================="

		print str("self.total_count = %d") % (self.total_count)

	def crawData2(self, url, tag_name):
		driver = webdriver.PhantomJS()
		driver.get(url);
		# time.sleep(2)
		# data = driver.find_element_by_tag_name(tag_name)
		data = driver.find_elements_by_class_name('code')
		for dt in data:
			print dt.text
		data2 = driver.find_elements_by_class_name('winner')
		for dt2 in data2:
			print dt2.text
		driver.quit()

	def crawData3(self, url, tag_name):
		driver = webdriver.PhantomJS()
		driver.get(url);
		data = driver.find_elements_by_tag_name('table')
		for dt in data:
			print dt.text
			print "====================================="
		driver.quit()

	def fetchUrl(self, url):
		url = str(self.baseurl) % (cid)
		res = requests.get(url)
		html = res.content
		try:
			html = html.decode('utf-8')
		except:
			pass
		# print(html)
		soup = BeautifulSoup(html, "lxml")
		# print(soup.prettify())
		# print(soup.find_all('a'))
		links = soup.find_all('a', href=re.compile('http://1.163.com'))
		for link in links:
			addr = link.get('href')
			if self.checkUrl(addr):
				pass
			else:
				print(str('---------------------fetchurl:') + addr)
				self.urls.append(addr)
				self.fetchUrl(addr)
            
	def saveToMongoDB(self, data):
		client = MongoClient('mongodb://198.52.117.75:27017/')
		db = client.duobao
		collection = db.winners
		collection.insert(data);
		client.close()
		
	def __unicode__(self):
		return self.baseurl

db = Duobao()
# db.getdata()
db.baseurl = str(db.baseurl) % (cid)
db.crawData(db.baseurl, 'table')
# db.fetchUrl('http://1.163.com')