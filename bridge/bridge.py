#!/usr/bin/python
# -*- coding : utf-8 -*-

"""
Bridge pattern:
Decouple an abstraction from its implementation so that the two can vary independently.
In this demo code, Window is an abstraction class that client defined. WindowImplFactory is a singleton factory that generates default WindowImpl in current platform. Now we suppose there are two platforms OS X and Ubuntu. When exchanging the platform, we don't change the client code and just to exchange different implementation of WindowImpl.
"""

#Abstraction class (client code)
class Window(object):
	def __init__(self):
		self.__impl = WindowImplFactory().get_window_impl()
	def draw_rectangle(self, top, left, length, height):
		self.__impl.draw_line(top, left, top, left + length)
		self.__impl.draw_line(top, left, top + height, left)
		self.__impl.draw_line(top, left + length, top + height, left + length)
		self.__impl.draw_line(top + height, left, top + height, left + length)

	def draw_text(self, text, font_size, top, left):
		for index, ch in enumerate(text):
			self.__impl.draw_character(ch, font_size, top, left + index * font_size)

#Refined Abstraction (client code)
class TransientWindow(Window):
	def __init__(self, engine):
		super(RacingCar, self).__init__(engine)

#Refined Abstraction (client code)
class ResizableWindow(Window):
	def __init__(self, engine):
		super(RacingCar, self).__init__(engine)

#One implementor on Mac X OS
class WindowOSXImpl(object):
	def draw_line(self, from_top, from_left, to_top, to_left):
		print("Draw a line from ({}, {}) to ({}, {}) on OS X.".format(from_top, from_left, to_top, to_left))
	def draw_character(self, ch, sz, top, left):
		print("Draw {} on position ({}, {}) with size {} on OS X.".format(ch, top, left, sz))

#Another implementor
class WindowUbuntuImpl(object):
	def draw_line(self, from_top, from_left, to_top, to_left):
		print("Draw a line from ({}, {}) to ({}, {}) on Ubuntu.".format(from_top, from_left, to_top, to_left))
	def draw_character(self, ch, sz, top, left):
		print("Draw {} on position ({}, {}) with size {} on Ubuntu.".format(ch, top, left, sz))

class WindowImplFactoryMeta(type):
	__instance = None
	def __call__(cls, *args, **kws):
		if cls.__instance == None:
			cls.__instance = super(WindowImplFactoryMeta, cls).__call__(*args, **kws)
		return cls.__instance

#WindowImpl Factory
class WindowImplFactory(metaclass=WindowImplFactoryMeta):
	def get_window_impl(self, *args, **kws):
		return self._impl.__call__(*args, **kws)
	def set_window_impl(self, impl):
		self._impl = impl


def main():
	#in MacX platform
	print("In OSX:==============")
	WindowImplFactory().set_window_impl(WindowOSXImpl)
	window = Window()
	window.draw_rectangle(10, 10, 20, 30)
	window.draw_text("OS X!", 5, 40, 10)

	#in Ubuntu platform
	print("In Ubuntu:==============")
	WindowImplFactory().set_window_impl(WindowUbuntuImpl)
	window = Window()
	window.draw_rectangle(10, 10, 20, 30)
	window.draw_text("Ubuntu!", 5, 40, 10)

if __name__ == '__main__':
	main()

"""
OUTPUT:
In OSX:==============
Draw a line from (10, 10) to (10, 30) on OS X.
Draw a line from (10, 10) to (40, 10) on OS X.
Draw a line from (10, 30) to (40, 30) on OS X.
Draw a line from (40, 10) to (40, 30) on OS X.
Draw O on position (40, 10) with size 5 on OS X.
Draw S on position (40, 15) with size 5 on OS X.
Draw   on position (40, 20) with size 5 on OS X.
Draw X on position (40, 25) with size 5 on OS X.
Draw ! on position (40, 30) with size 5 on OS X.
In Ubuntu:==============
Draw a line from (10, 10) to (10, 30) on Ubuntu.
Draw a line from (10, 10) to (40, 10) on Ubuntu.
Draw a line from (10, 30) to (40, 30) on Ubuntu.
Draw a line from (40, 10) to (40, 30) on Ubuntu.
Draw U on position (40, 10) with size 5 on Ubuntu.
Draw b on position (40, 15) with size 5 on Ubuntu.
Draw u on position (40, 20) with size 5 on Ubuntu.
Draw n on position (40, 25) with size 5 on Ubuntu.
Draw t on position (40, 30) with size 5 on Ubuntu.
Draw u on position (40, 35) with size 5 on Ubuntu.
Draw ! on position (40, 40) with size 5 on Ubuntu.
"""