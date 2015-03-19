#coding=utf-8
import splinter
import time
import random
import requests
import re
from bs4 import BeautifulSoup
from splinter import Browser
from selenium import webdriver
import time
from pymongo import MongoClient

class Duobao:
	filter1 = "\?cid="
	filter2 = "index.do\?cid="
	baseurl = "http://1.163.com/user/index.do?cid=41022423"
	urls = []
	def getdata(self):
		url = str(self.baseurl)
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
		driver = webdriver.PhantomJS()
		driver.get(url);
		data = driver.find_elements_by_tag_name('table')
		for dt in data:
			print dt.text
			print "====================================="
		driver.quit()

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
	def __unicode__(self):
		return self.baseurl

db = Duobao()
# db.getdata()
db.crawData(db.baseurl, 'table')