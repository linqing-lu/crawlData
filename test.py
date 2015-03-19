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

class Duobao:
	baseurl = "http://1.163.com/user/win.do?cid=43279246"
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
		links = soup.find_all('a', href=re.compile('http'))
		for link in links:
			addr = link.get('href')
			if self.checkUrl(addr):
				pass
			print(str('获取链接：') + addr)
			self.getdatas(addr)
			# print(addr)
	def getdatas(self, url):
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
		links = soup.find_all('a')
		for link in links:
			print(link.get('href'))	
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

	def crawData(self, url):
		driver = webdriver.PhantomJS()
		driver.get(url);
		time.sleep(2)
		data = driver.find_element_by_tag_name('body')
		print data.text
		driver.quit()
						
	def __unicode__(self):
		return self.baseurl

# dt = Duobao()
# dt.getdata()