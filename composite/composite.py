#!/usr/bin/python
# -*- coding : utf-8 -*-

"""
Composite Pattern:
Compose objects into tree structures to represent part-whole hierarchies. Composite lets clients treat individual objects and compositions of objects uniformly.
In this piece of code, we animate the structure of HTML document, which is a tree structure. Every element is a node and some of them can have children elements and have attributes.
"""
import functools

#component class
class HTMLElement(object):
	def __init__(self, parent=None):
		if parent and not isinstance(parent, HTMLTag):
			raise ValueError("The parent must be a HTML tag.")
		self._parent = parent

	@property
	def parent(self):
	    return self._parent

#Composite class
class HTMLTag(HTMLElement):
	def __init__(self, tag_type, **attrs):
		super(HTMLTag, self).__init__(None)
		self._tag_type = tag_type
		self._attrs = attrs
		self._children = []

	@property
	def tag_type(self):
	    return self._tag_type

	def append(self, child):
		if isinstance(child, HTMLContent) or isinstance(child, str):
			return self.append_content(child)
		if isinstance(child, HTMLEmptyTag) or isinstance(child, HTMLTag):
			return self.append_child(child)
		raise ValueError("Can not add the child.")

	def append_child(self, child):
		child._parent = self
		self._children.append(child)
		return self
		
	def append_content(self, content):
		if len(self._children) and isinstance(self._children[len(self._children) - 1], HTMLContent):
			self._children[len(self._children) - 1].append(content)
		child = HTMLContent(content, self)
		self._children.append(child)	
		return self

	def __str__(self):
		return '<' + self._tag_type + \
				(" " + functools.reduce(lambda x, y: x + ' ' + y, [x + "='" + y + "'" for x, y in self._attrs.items()]) if len(self._attrs) > 0 else '') \
						+ '>' + ((functools.reduce(lambda x, y: x + y, map(lambda x : x.__str__(), self._children))) if len(self._children) > 0 else '') \
								+ '</' + self._tag_type + '>'

#composite class
class HTMLEmptyTag(HTMLElement):
	def __init__(self, tag_type, **attrs):
		super(HTMLEmptyTag, self).__init__(None)
		self._tag_type = tag_type
		self._attrs = attrs

	@property
	def tag_type(self):
	    return self._tag_type

	def __str__(self):
		return '<' + self._tag_type + (" " + functools.reduce(lambda x, y: x + ' ' + y, [x + "='" + y + "'" for x, y in self._attrs.items()]) if len(self._attrs) > 0 else '') + '/>'


#Composite class
class HTMLContent(HTMLElement):
	def __init__(self, content, sup):
		super(HTMLContent, self).__init__(sup)
		if not isinstance(content, str):
			raise ValueError("The content must be a string.")
		self._content = content

	@property
	def content(self):
	    return self._content

	@content.setter
	def content(self, content):
		if not isinstance(content, str):
			raise ValueError("The content must be a string.")
		self._content = content

	def __str__(self):
		return self._content

	def append(content):
		if isinstance(content, HTMLContent):
			self._content += content._content
		elif isinstance(content, str):
			self._content += content
		else:
			raise ValueError("The content must be a string.")

def main():
	html = HTMLTag("html")
	html.append_child(HTMLTag("head").append(HTMLTag("title").append_content("Python design pattern: composite")).append(HTMLTag("srcipt", src="./srcipt/jquery.min.js")))
	html.append_child(HTMLTag("body").append(HTMLTag("p", width="100%", height="500px").append("Is composite a design pattern?").append_child(HTMLEmptyTag("br")).append("Yes, it is.")).append(HTMLTag("div", width="100%", height="400px").append(HTMLEmptyTag("img", href="./img/a.jpg"))))

	print(html)

if __name__ == '__main__':
	main()

"""
OUTPUT:
<html><head><title>Python design pattern: composite</title><srcipt src='./srcipt/jquery.min.js'></srcipt></head><body><p width='100%' height='500px'>Is composite a design pattern?<br/>Yes, it is.</p><div width='100%' height='400px'><img href='./img/a.jpg'/></div></body></html>
"""	
