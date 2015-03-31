#!/usr/bin/python
# -*- coding : utf-8 -*-

"""
Factory method is a design pattern. It is spposed to design an interface for creating an object, but let subclasses decide which class to instantiate. It lets a class defer instantiation to subclasses.
"""
class FigureManipulator(object):
	def __init__(self, figure):
		self.__figure = figure
	def down_click(self, target=2):
		print("Default manipulate: move down figure to: {} pixels.".format(target))
	def up_click(self, target=2):
		print("Default manipulate: move up figure to: {} pixels.".format(target))
	def drag(self, target={"left": 5, "top": -5}):
		print("Default manipulate: move figure left to {} pixels and up to {} pixels.".format(target['left'], target['top']))

class LineManipulator(FigureManipulator):
	def __init__(self, figure):
		self.__figure = figure
	def down_click(self, target=2):
		print("Line manipulate: move down figure to: {} pixels.".format(target))
	def up_click(self, target=2):
		print("Line manipulate: move up figure to: {} pixels.".format(target))
	def drag(self, target={"left": 5, "top": -5}):
		print("Line manipulate: move figure left to {} pixels and up to {} pixels.".format(target['left'], target['top']))

class TextManipulator(FigureManipulator):
	def __init__(self, figure):
		self.__figure = figure
	def down_click(self, target=2):
		print("Text manipulate: move down figure to: {} pixels.".format(target))
	def up_click(self, target=2):
		print("Text manipulate: move up figure to: {} pixels.".format(target))
	def drag(self, target={"left": 5, "top": -5}):
		print("Text manipulate: move figure left to {} pixels and up to {} pixels.".format(target['left'], target['top']))

class Figure(object):
	def __init__(self, name, url):
		self._name = name
		self._url = url

	def get_manipulator(self):
		return FigureManipulator(self)

class LineFigure(Figure):
	def __init__(self, name, url, line_pos):
		super(LineFigure, self).__init__(name, url)
		self._line_pos = line_pos

	def get_manipulator(self):
		return LineManipulator(self)

class TextFigure(Figure):
	def __init__(self, name, url, text):
		super(TextFigure, self).__init__(name, url)
		self._text = text

	def get_manipulator(self):
		return TextManipulator(self)

if __name__ == '__main__':
	for figure in [Figure("a", "http://www.a.com/pic/a.jpg"), LineFigure("b", "http://www.a.com/pic/b.jpg", {"left": 6, "top": -6}), TextFigure("c", "http://www.a.com/pic/c.jpg", "Fig C")]:
		print("For figure: {}".format(figure._name))
		manipulator = figure.get_manipulator()
		manipulator.up_click(10)
		manipulator.down_click(5)
		manipulator.drag({"left": 10, "top": -15})
		print("=" * 10)



