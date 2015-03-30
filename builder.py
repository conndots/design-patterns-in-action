#!/usr/bin/python
# -*- coding : utf-8 -*-

class DocDirector:
	"""
	DocDirector class
	Constructs a product/products using the specified Builder implementation.
	In this example, it is the interface the client calls to construct a specified document.
	"""
	def __init__(self):
		self.__builder = SummaryDocBuilder()

	def build_document(self):
		self.__builder.new_document()

	def append_to_document(self, text):
		self.__builder.append_to_document(text)

	#The product is just a string
	def get_document(self):
		return self.__builder._document

	def set_builder(self, builder):
		self.__builder = builder

#the base class of a builder
class DocBuilder:
	"""
	The base interface for a builder.
	It specifies a builder that can build part of the product(document)
	"""
	def __init__(self):
		self._document = None
	def new_document(self):
		self._document = ""

class SummaryDocBuilder(DocBuilder):
	#Simplely replace the line break to a space
	def append_to_document(self, text):
		for ch in text:
			if ch == '\n':
				self._document += " "
			else:
				self._document += ch

class HTMLDocBuilder(DocBuilder):
	#replace the line break to a <br> tag.
	def append_to_document(self, text):
		for ch in text:
			if ch == '\n':
				self._document += "<br>"
			else: 
				self._document += ch

class MarkdownBuilder(DocBuilder):
	#replace the line break to "  \n" as the MD syntax.
	def append_to_document(self, text):
		for ch in text:
			if ch == '\n':
				self._document += "  \n"
			else:
				self._document += ch

if __name__ == '__main__':
	dir = DocDirector()
	for builder in [SummaryDocBuilder(), HTMLDocBuilder(), MarkdownBuilder()]:
		dir.set_builder(builder)
		dir.build_document()
		dir.append_to_document("This is a document.\nThis is definitely a docuemnt.\nSo,why bother?")
		dir.append_to_document("\nI don't want to say it again.\nYou must listen!\n")
		print("Document built by {}:\n{}".format(builder.__class__.__name__, dir.get_document()))
		print("="*20)

"""
OUTPUT:
Document built by SummaryDocBuilder:
This is a document. This is definitely a docuemnt. So,why bother? I don't want to say it again. You must listen! 
====================
Document built by HTMLDocBuilder:
This is a document.<br>This is definitely a docuemnt.<br>So,why bother?<br>I don't want to say it again.<br>You must listen!<br>
====================
Document built by MarkdownBuilder:
This is a document.  
This is definitely a docuemnt.  
So,why bother?  
I don't want to say it again.  
You must listen!  

====================
"""


