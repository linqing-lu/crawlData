#coding=utf-8
import splinter
import time
import random
import requests
import re
import codecs
import hashlib
from pymongo import MongoClient

base_url = "http://1.163.com/user/duobaoRecord/get.do?"
user_agent = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) "
              "AppleWebKit/537.36 (KHTML, like Gecko) "
              "Chrome/36.0.1985.143 Safari/537.36")

post_headers = {"User-Agent": user_agent,"Referer": "http://1.163.com"}

class DuobaoRecord(object):
	"""docstring for DuobaoRecord"""
	def __init__(self, cid):
		super(DuobaoRecord, self).__init__()
		self.cid = cid
		self.total_cost = 0
		self.total_win = 0
		self.total_count = 0
		self.cur_count = 0
		self.all_lsit = []
		self.session = requests.Session()
		r = self.session.get("http://1.163.com")
		if r.status_code == 200:
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
	def queryRecord(self):
		page_num = 1
		page_size = 100
		totalCnt = 0
		info = {'cid':self.cid, 'pageSize':page_size,'pageNum':page_num,'t':self.t,'token':self.token}
		info['status'] = 9
		info['region'] = 0

		running = True
		while running:
			info['pageNum'] = page_num
			info['totalCnt'] = totalCnt
			info['pageSize'] = page_size
			res = self.session.get(base_url, params=info)
			if res.status_code == 200:
				# print res.headers
				result = res.json()['result']
				totalCnt = result['totalCnt']
				if totalCnt <= 0:
					running = False
					break
				page_num = result['pageNum']
				page_size = result['pageSize']
				rlist = result['list']
				self.cur_count = self.cur_count + len(rlist)
				for rec in rlist:
					if int(rec['type']) == 0:
						self.total_cost = self.total_cost + rec['num']
						self.total_count = self.total_count + 1
						if rec['ownerId'] == self.cid:
							self.total_win = self.total_win + rec['goods']['price']
					# print rec['type']
					# print rec['status']
				progress = float(self.cur_count)/float(totalCnt) * 100
				print ("%0.2f%%") % (progress)
				if totalCnt > page_size * page_num:
					page_num = page_num + 1
				else:
					running = False
			else:
				running = False
	def queryRecord2(self):
		page_num = 1
		page_size = 100
		totalCnt = 0
		info = {'cid':self.cid, 'pageSize':page_size,'pageNum':page_num,'t':self.t,'token':self.token}
		info['status'] = 9
		info['region'] = 0

		running = True
		while running:
			info['pageNum'] = page_num
			info['totalCnt'] = totalCnt
			info['pageSize'] = page_size
			res = self.session.get(base_url, params=info)
			if res.status_code == 200:
				# print res.headers
				result = res.json()['result']
				totalCnt = result['totalCnt']
				if totalCnt <= 0:
					running = False
					break
				page_num = result['pageNum']
				page_size = result['pageSize']
				rlist = result['list']
				self.cur_count = self.cur_count + len(rlist)
				self.all_lsit.extend(rlist)
				progress = float(self.cur_count)/float(totalCnt) * 100
				print ("%0.2f%%") % (progress)
				if totalCnt > page_size * page_num:
					page_num = page_num + 1
				else:
					running = False
			else:
				running = False
	def __unicode__(self):
		return self.cid

def main():
	dr = DuobaoRecord(13578716)
	dr.queryRecord2()
	print len(dr.all_lsit)
	# save_data = {'_id': dr.cid}
	# save_data['total_cost'] = dr.total_cost
	# save_data['total_count'] = dr.total_count
	# save_data['total_win'] = dr.total_win
	# save_data['total_profit'] = dr.total_win - dr.total_cost
	# print save_data

if __name__ == '__main__':
	main()
