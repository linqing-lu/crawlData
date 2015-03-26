#coding=utf-8

A = 0
B = 1
C = 28888
D = 10000001
x = 10006938
E = 23085 #预测数
# （A + E) % C = x - D
# A = x1 + x2 + ... + x50 = Xm + Xn
# 在一定时间范围内(比如说一个小时内)求A的可能值
# 先求x-D，假设E的是一个确定值，求A的可能值
# 用程序抓取并计算出Xm的值，计算出Xn需要的值
# 对Xn的值施加影响

class CalcNumber(object):
	"""docstring for CalcNumber"""
	def __init__(self, x):
		super(CalcNumber, self).__init__()
		self.x = x
		self.number = x - D

	def calc(self):
		