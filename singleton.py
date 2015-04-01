#!/usr/bin/python
# -*- coding : utf-8 -*-

"""
Singleton pattern: 
ensure a class only has one instance, and provide a global point of access to it.
There is a discussion here: http://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
The metaclass in python is useful here. I use the grammar defined in Python 3.
"""

class SingletonMeta(type):
	__singletons = {}
	def __call__(cls, *args, **kws):
		if cls not in cls.__singletons:
			cls.__singletons[cls] = super(Singleton, cls).__call__(*args, **kws)
		return cls.__singletons[cls]

class A(metaclass=SingletonMeta):
	def __init__(self):
		print("initiate the singleton class object: " + A.__name__)
		self.a = 5
		self.b = 6

class B(metaclass=Singleton):
	def __init__(self):
		print("initiate the singleton class object: " + B.__name__)

if __name__ == '__main__':
	prevA = None
	prevB = None
	for i in range(5):
		a = A()
		b = B()
		if prevA != None and prevB != None:
			print("{}: {} and {}".format(i, a == prevA, b == prevB))
		prevA = a
		prevB = b
"""
OUTPUT:
initiate the singleton class object: A
initiate the singleton class object: B
1: True and True
2: True and True
3: True and True
4: True and True
"""
