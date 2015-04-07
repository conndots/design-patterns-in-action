#!/usr/bin/python
# -*- coding : utf-8 -*-

"""
Decorator pattern. It is a feature for python.
Adding additional responsibilities to an object or a function.
In this demo, every time son makes a plan or write a dairy, the decorator will send a message to his mum.
"""

from functools import wraps
from datetime import datetime

def peep(text):
	def decorator(func):
		@wraps(func)
		def wrapper(*args, **kw):
			info = '{} {}[{}] : '.format(datetime.now().__str__(), \
				func.__name__, text) + ('\n\targuments: ' + args.__str__() 
					+ " " + kw.__str__())
			send_to_mum(info)
			return func(*args, **kw)
		return wrapper
	return decorator

def send_to_mum(info):
	print('[Sent to mum]{}'.format(info))

class Dairy:
	@peep('Son\'s dairy')
	def today(self, **kw):
		return 'Today\'s Dairy: ' + kw.__str__()

	@peep('Son\'s dairy')
	def plan(self, *plans):
		return 'Plan to: ' + plans.__str__()

if __name__ == '__main__':
	dairy = Dairy()
	print(dairy.today(mood='good', weather='rainy'))
	print(dairy.plan('Go to Sillcon Valley', 'Fall in love with my goddess'))

"""
OUTPUT:
[Sent to mum]2015-04-07 19:31:45.144732 today[Son's dairy] : 
	arguments: (<__main__.Dairy object at 0x0000000002C0AD68>,) {'weather': 'rainy', 'mood': 'good'}
Today's Dairy: {'weather': 'rainy', 'mood': 'good'}
[Sent to mum]2015-04-07 19:31:45.144732 plan[Son's dairy] : 
	arguments: (<__main__.Dairy object at 0x0000000002C0AD68>, 'Go to Sillcon Valley', 'Fall in love with my goddess') {}
Plan to: ('Go to Sillcon Valley', 'Fall in love with my goddess')
"""