import splinter
import time
import random
import requests
import re
from bs4 import BeautifulSoup
from splinter import Browser
from selenium import webdriver
from pymongo import MongoClient

class BloomFilter(object):
	"""docstring for BloomFilter"""
	def __init__(self, arg):
		super(BloomFilter, self).__init__()
		self.arg = arg
