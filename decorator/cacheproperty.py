#!/usr/bin/python
# -*- coding : utf-8 -*-

"""
Decorator pattern. It is a feature for python.
Adding additional responsibilities to an object or a function.
In this demo, every time son makes a plan or write a dairy, the decorator will send a message to his mum.
Another example from https://github.com/brennerm/PyTricks/blob/master/cacheproperty.py
"""
class PropertyCache:
	"a decorator to cache property"
	def __init__(self, func):
		self.func = func

	def __get__(self, obj, cls):
		if not obj:
			return self
		value = self.func(obj)
		setattr(obj, self.func.__name__, value)
		return value

class A:
	def __init__(self):
		self._property_to_be_cached = 'result'

	@PropertyCache
	def property_to_be_cached(self):
		print('compute')
		return self._property_to_be_cached

if __name__ == '__main__':
	test = A()
	print(test.property_to_be_cached)
	print(test.property_to_be_cached)
	print(test.property_to_be_cached)

"""
OUTPUT:
compute
result
result
result
"""