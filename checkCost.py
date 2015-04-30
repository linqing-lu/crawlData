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

base_url_code = "http://1.163.com/code/get.do?"
base_url = "http://1.163.com/record/getDuobaoRecord.do?"
user_agent = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) "
              "AppleWebKit/537.36 (KHTML, like Gecko) "
              "Chrome/36.0.1985.143 Safari/537.36")
login_url = "https://reg.163.com/login.jsp"
logininfo = {"username": "", "password": "","product": "mail163","url":"http://1.163.com","savelogin":""}

post_headers = {"User-Agent": user_agent,"Referer": "http://1.163.com"}
def list_cmp(a1, a2):
	return 0 - cmp(a1['rid'], a2['rid'])
class Goods(object):
	def __init__(self, gid, period, collection):
		super(Goods, self).__init__()
		self.gid = gid
		self.period = period
		self.collection = collection
		self.cur_count = 0
		self.all_list = []
		self.session = requests.Session()
		self.login_session = requests.Session()
		url = str("http://1.163.com/detail/%02d-%02d-%02d-%02d-%02d.html") \
		% (gid/100, gid%100, period/10000, period%10000/100, period%100)
		print url
		r = self.session.get("http://1.163.com",headers=post_headers)
		if r.status_code == 200:
			print r.headers
			cookie = r.headers['set-cookie']
			strs = cookie.split(';')
			otoken = strs[0]
			strtime = strs[2].split('=')[1]
			ttime = time.strptime(strtime, "%a, %d-%b-%Y %H:%M:%S GMT")
			self.t = time.mktime(ttime)
			self.token = otoken.split('=')[1]
			print 'create session success'
		else:
			print 'create session failed'
	def login(self):
		logininfo['username'] = 'xxx@163.com'
		logininfo['password'] = 'xxxx'
		login_res = self.login_session.post(login_url, data=logininfo,headers=post_headers,)
		print login_res.status_code
		if login_res.status_code == 200:
			return True
		else:
			return False
	def checkCost(self):
		page_size = 50
		page_num = 1
		totalCnt = 0;
		info = {'gid':self.gid,'period':self.period,'t':self.t,'token':self.token}
		running = True
		max_rid = self.getMaxRid()
		while running:
			info['pageSize'] = page_size
			info['pageNum'] = page_num
			info['totalCnt'] = totalCnt
			res = self.session.get(base_url, params=info)
			if res.status_code == 200:
				result = res.json()
				result = result['result']
				totalCnt = result['totalCnt']
				if totalCnt <= 0:
					running = False
					break
				page_size = result['pageSize']
				page_num = result['pageNum']
				costlist = result['list']
				self.cur_count = self.cur_count + len(costlist)
				print max_rid
				costlist.sort(cmp=list_cmp)
				for cost in costlist:
					print cost['rid']
					if int(cost['rid']) <= int(max_rid):
						running = False
						break
					costinfo = {}
					costinfo['cost_id'] = cost['rid']
					costinfo['cid'] = int(cost['user']['cid'])
					costinfo['cost_num'] = cost['num']
					costinfo['cost_time'] = cost['time']
					costinfo['uid'] = cost['user']['uid']
					costinfo['ip_address'] = cost['user']['IPAddress']
					costinfo['nickname'] = cost['user']['nickname']
					costinfo['gid'] = self.gid
					costinfo['period'] = self.period
					costinfo['_id'] = str("%d_%d_%d") % (self.gid, self.period, costinfo['cid'])
					# print costinfo
					# break;
					try:
						self.collection.insert(costinfo)
					except Exception, e:
						costinfo_t = self.collection.find_one({"_id": costinfo['_id']})
						costinfo['cost_num'] = costinfo['cost_num'] + costinfo_t['cost_num']
						if max_rid <= 0:
							costinfo['cost_id'] = costinfo_t['cost_id']
						self.collection.save(costinfo)
						print costinfo
				if not running:
					print ("100.00%%")
					break
				progress = float(self.cur_count)/float(totalCnt) * 100
				print ("%0.2f%%") % (progress)
				if totalCnt > page_size * page_num:
					page_num = page_num + 1
				else:
					running = False
			else:
				running = False
	def checkCost2(self):
		page_size = 50
		page_num = 1
		totalCnt = 0;
		info = {'gid':self.gid,'period':self.period,'t':self.t,'token':self.token}
		running = True
		max_rid = self.getMaxRid()
		while running:
			info['pageSize'] = page_size
			info['pageNum'] = page_num
			info['totalCnt'] = totalCnt
			res = self.session.get(base_url, params=info)
			if res.status_code == 200:
				result = res.json()
				result = result['result']
				totalCnt = result['totalCnt']
				if totalCnt <= 0:
					running = False
					break
				page_size = result['pageSize']
				page_num = result['pageNum']
				costlist = result['list']
				self.cur_count = self.cur_count + len(costlist)
				costlist.sort(cmp=list_cmp)
				self.all_list.extend(costlist)
				progress = float(self.cur_count)/float(totalCnt) * 100
				print ("%0.2f%%") % (progress)
				if totalCnt > page_size * page_num:
					page_num = page_num + 1
				else:
					running = False
			else:
				running = False
	def getMaxRid(self):
		data = self.collection.find({"gid":self.gid,"period":self.period},{"cost_id": 1}).sort([("cost_id", -1)]).limit(1)
		print data
		retVal = 0
		try:
			maxIssue = data[0]['cost_id']
			retVal = int(maxIssue)
			return retVal
		except Exception, e:
			retVal = 0
			return retVal
	def getNumbers(self, cid):
		info = {'gid':self.gid,'period':self.period,'t':self.t,'token':self.token}
		info['cid'] = cid
		res = self.login_session.get(base_url_code, params=info)
		if res.status_code == 200:
			result = res.json()
			result = result['result']
			codelist = result['list']
			for codes in codelist:
				for code in codes['code']:
					print int(code);


def main():
	client = MongoClient("mongodb://23.236.78.15", 27017)
	db = client.duobao
	db.authenticate('test', 'duobao')
	# for i in range(1, 5):
	# 	g = Goods(117, 25-i, db.costs)
	# 	g.checkCost()
	# 	g = Goods(112, 185-i, db.costs)
	# 	g.checkCost()
	# 	g = Goods(181, 50-i, db.costs)
	# 	g.checkCost()
	# 	print len(g.all_list)
	# print g.all_list
	# print g.getMaxRid()
	g = Goods(112, 181, db.costs)
	# g.checkCost()
	g.getNumbers(47803250)
	

	db.logout()
	client.close()
if __name__ == '__main__':
	main()		