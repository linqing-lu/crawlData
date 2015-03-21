#coding=utf-8
import Queue
import threading
from threading import Thread
import time

class MyThread(Thread):
	"""docstring for MyThread"""
	def __init__(self, threadID, name, q, queueLock, collection):
		super(MyThread, self).__init__()
		self.threadID = threadID
		self.name = name
		self.q = q
		self.exitFlag = 0
		self.queueLock = queueLock
		self.collection = collection

	def run(self):
		while not self.exitFlag:
			self.processData()
		print str("thread %d exit") % (self.threadID)

	def processData(self):
		self.queueLock.acquire()
		if not self.q.empty():
			data = self.q.get()
			self.queueLock.release()
			collection.save(data)
		else:
			self.queueLock.release()
			time.sleep(1)
