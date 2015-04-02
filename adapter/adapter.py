#!/usr/bin/python
# -*- coding : utf-8 -*-

"""
adapter(wrapper) pattern:
Convert the interface of a class into another interface clients expect. Adapter lets classes work together that couldn't otherwise bacause of incompatible interfaces.
References:
http://ginstrom.com/scribbles/2008/11/06/generic-adapter-class-in-python/
"""
class Adapter(object):
	def __init__(self, obj, **adapted_methods):
		self.__obj = obj
		self.__dict__.update(adapted_methods)
	def __getattr__(self, attr):
		return getattr(self.__obj, attr)

class Cat(object):
	def meow(self):
		print("I'm a cat, and I'm meowing.")

class Dog(object):
	def bark(self):
		print("I'm a dog, and I'm barking.")



def main():
	cat = Cat()
	dog = Dog()
	creatures = []
	creatures.append(Adapter(cat, make_noise=cat.meow))
	creatures.append(Adapter(dog, make_noise=dog.bark))
	for creature in creatures:
		creature.make_noise()
		if(hasattr(creature, 'meow')):
				creature.meow()
		elif(hasattr(creature, 'bark')):
				creature.bark()

if __name__ == '__main__':
	main()

"""
OUTPUT:
I'm a cat, and I'm meowing.
I'm a cat, and I'm meowing.
I'm a dog, and I'm barking.
I'm a dog, and I'm barking.
"""
