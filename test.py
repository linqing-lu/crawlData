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

class Duobao(object):
	filter1 = "\?cid="
	filter2 = "index.do\?cid="
	filter3 = "win.do\?cid="
	baseurl = "http://1.163.com/user/index.do?cid=%d"
	winurl = "http://1.163.com/user/win.do?cid=%d"
	urls = []
	total_count = 0
	total_cost = 0
	total_win = 0
	cid = 15191257

	client = 0
	db = 0

	def __init__(self, cid):
		super(Duobao, self).__init__()
		self.cid = cid
		self.client = MongoClient('mongodb://198.52.117.75:27017/')
		self.db = self.client.duobao
		self.db.authenticate('test', 'duobao')

	def getdata(self):
		url = str(self.baseurl) % (self.cid)
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
		for turl in self.urls:
			if turl == url:
				return True
		return False
	def browseUrl(self, url):
		with Browser('chrome') as browser:
			browser.visit(url)
			sp = BeautifulSoup(browser.html, "lxml")
			print(sp.prettify())

	def crawData(self, tag_name):
		url = str(self.baseurl) % (self.cid)
		self.total_cost = 0
		self.total_count = 0
		driver = webdriver.PhantomJS()
		driver.get(url);
		running = True
		# fp = codecs.open("/Users/lm/test.txt", 'a+', 'utf-8')
		data = driver.find_elements_by_tag_name('table')
		while running:
			self.dealData(data, 0)
			running = len(data) > 10
			print running
			if running:
				btn_next = driver.find_element_by_class_name('w-pager-next')
				btn_next.click()
				time.sleep(1)
				data = driver.find_elements_by_tag_name('table')
		# fp.close()
		driver.quit()

	def dealData(self, data, fp):
		count = 0;
		for dt in data:
			if count == 0:
				count = count + 1
				continue
			# print dt.text
			total_price = 0
			winner_price = 0
			winner_info = {}
			try:
				col4 = dt.find_element_by_class_name('col4')
				# print col4.text
				prices = re.findall(r'(\w*[0-9]+)\w*', col4.text)
				# print prices
				self.total_cost = self.total_cost + int(prices[0])
				self.total_count = self.total_count + 1
			except Exception, e:
				pass

			winned = False
			try:
				col3 = dt.find_element_by_class_name('col3')
				if col3.text == ("已揭晓").decode('utf8'):
					winned = True
			except Exception, e:
				raise e

			if winned:
				try:
					winner = dt.find_element_by_class_name('winner')
					# print winner.text
					winner_name = winner.find_element_by_class_name('name')
					winner_url = winner_name.find_element_by_tag_name('a').get_attribute('href')
					temp = re.findall(r'cid=(\w*[0-9]+)\w*', winner_url)
					winner_cid = int(temp[0])
					winner_vote = winner_name.find_element_by_class_name('txt-dark')
					winner_price = int(winner_vote.text)
					winner_info['cost'] = winner_price
					winner_info['winner_cid'] = winner_cid
					# print winner_price	
				except Exception, e:
					raise e

				try:
					col2 = dt.find_element_by_class_name('col2')
					goods_price = col2.find_element_by_class_name('w-goods-price')
					# print goods_price.text
					total_price = re.findall(r'(\w*[0-9]+)\w*', goods_price.text)
					winner_info['price'] = int(total_price[0])
				except Exception, e:
					raise e

				try:
					col2 = dt.find_element_by_class_name('col2')
					goods_name = col2.find_element_by_class_name('w-goods-title')
					goods_name_a = goods_name.find_element_by_tag_name('a')
					goods_title = goods_name_a.get_attribute('title')
					numbers = re.findall(r'(\w*[0-9]+)\w*', goods_name_a.text)
					goods_issue = int(numbers[0])
					winner = col2.find_element_by_class_name('winner')
					# print goods_title
					m = hashlib.md5()
					m.update(goods_title.encode('utf8'))
					winner_info['_id'] = str("%s_%d") % (m.hexdigest(), goods_issue)
					winner_info['issue'] = goods_issue
					winner_info['title'] = goods_title

				except Exception, e:
					raise e
				self.saveToMongoDB(winner_info, self.db.detail)
			# print "====================================="

		print str("self.total_cost = %d") % (self.total_cost)
	def crawWinData(self, tag_name):
		url = str(self.winurl) % (self.cid)
		self.total_win = 0
		driver = webdriver.PhantomJS()
		driver.get(url);
		running = True
		# fp = codecs.open("/Users/lm/test.txt", 'a+', 'utf-8')
		data = driver.find_elements_by_class_name('w-goodsList-item')
		while running:
			self.dealWinData(data, 0)
			running = len(data) >= 12
			print running
			if running:
				btn_next = driver.find_element_by_class_name('w-pager-next')
				btn_next.click()
				time.sleep(1)
				data = driver.find_elements_by_class_name('w-goodsList-item')
		# fp.close()
		driver.quit()
	def dealWinData(self, data, fp):
		for dt in data:
			# print dt.text
			#获取title
			goods_info = {}
			try:
				goods_name = dt.find_element_by_class_name('w-goods-title')
				goods_name_a = goods_name.find_element_by_tag_name('a')
				goods_title = goods_name_a.get_attribute('title')
				# print goods_title
				m = hashlib.md5()
				m.update(goods_title.encode('utf8'))
				goods_info['_id'] = m.hexdigest()
				goods_info['title'] = goods_title
			except Exception, e:
				raise e
			#获取price
			try:
				goods_price = dt.find_element_by_class_name('w-goods-price')
				price = re.findall(r'(\w*[0-9]+)\w*', goods_price.text)
				goods_info['price'] = int(price[0]);
				self.total_win = self.total_win + goods_info['price']
			except Exception, e:
				raise e
			print goods_info
			self.saveToMongoDB(goods_info, self.db.goods)

	def saveToMongoDB(self, data, collection):
		collection.save(data);

	def saveCostDetail(self):
		print self.total_cost
		if self.total_cost > 0:
			save_data = {"_id": self.cid, "total_cost": self.total_cost, "total_count": self.total_count, "total_win": self.total_win}
			print save_data
			self.saveToMongoDB(save_data, self.db.winners)
	def uninit(self):
		self.db.logout()
		self.client.close()

	def __unicode__(self):
		return self.baseurl

def searchUserInfo(cid):
	print str("searchUserInfo %d") % (cid)
	db = Duobao(cid)
	# db.getdata()
	db.crawData('table')
	db.crawWinData('w-goodsList-item')
	db.saveCostDetail()
	db.uninit()

def main():
	client = MongoClient('mongodb://198.52.117.75:27017/')
	db = client.duobao
	db.authenticate('test', 'duobao')
	collection = db.users
	cid_data = collection.find_one({"searched": 0})
	print cid_data
	while cid_data['searched'] == 0:
		cid_data['searched'] = 1
		collection.save(cid_data)
		searchUserInfo(int(cid_data['_id']))
		cid_data = collection.find_one({"searched": 0})

	client.close()
if __name__ == '__main__':
	main()
