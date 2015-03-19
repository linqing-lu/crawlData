import splinter
import time
import random
import requests
import re
from bs4 import BeautifulSoup
from splinter import Browser
from selenium import webdriver
from pymongo import MongoClient

class Fetcher(object):
	"""docstring for Fetcher"""
	def __init__(self, arg):
		super(Fetcher, self).__init__()
		self.arg = arg
