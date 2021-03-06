#coding=utf-8
import time
import datetime

A = 0
B = 1
C = 28888
D = 10000001
E = 68978 #预测数
MAXNUM = 235959999
MINNUM = 0
MAXNUM2 = 99999
MINNUM2 = 0
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
		now = datetime.datetime.now()
		now_num_str = str("%02d%02d%02d%03d") % (now.hour, now.minute, now.second, now.microsecond/1000)
		print (now_num_str)
		now_num = int(now_num_str);

		now_num_str = str("%02d%02d%02d%03d") % (now.hour + 1, now.minute, now.second, now.microsecond/1000)

		max_num = int(now_num_str)*50 + MAXNUM2
		
		min_num = now_num * 50 + E;

		begin_num = (self.number - min_num%C) + min_num
		print begin_num
		print begin_num%C
		print self.number
		numbers = [begin_num]

		while begin_num <= max_num:
			begin_num = begin_num + C
			# print begin_num
			# print begin_num%C
			numbers.append(begin_num)
			if begin_num - E == 9222232432:
				break
		print numbers
		print len(numbers)

def main():
	c = CalcNumber(10003459)
	c.calc()

if __name__ == '__main__':
	main()


		