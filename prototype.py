"""
Prototype pattern: Specify the kinds of objects to create using a prototypical instance, and create new objects by copying this prototype. Please notice the difference between the concept of shallow copy and deep copy.
"""

import copy

class PostcardPrototypes:
	def __init__(self):
		self.__prototypes = {}

	def register_prototype(self, key, prototype):
		self.__prototypes[key] = prototype

	def unregister_prototype(self, key):
		del self.__prototypes[key]

	def clone_prototype(self, key, **attrs):
		clone = copy.deepcopy(self.__prototypes.get(key))
		if clone == None:
			return None
		clone.__dict__.update(attrs)
		return clone

class Postcard:
	def __init__(self, receiv, send, content):
		self.receiv = receiv
		self.send = send
		self.content = content

	def __str__(self):
		return "({} <- {} - {})".format(self.receiv, self.content, self.send)

if __name__ == '__main__':
	mgr = PostcardPrototypes()
	postcard = Postcard("Jim", "Lee", "Hello")
	mgr.register_prototype("basic", postcard)
	birthcard = mgr.clone_prototype("basic", receiv="Mark", send="Bill", content="Happy birthday!")
	weddingcard = mgr.clone_prototype("basic", receiv="Lucy", send="Phoebe", content="Happy forever!")

	for card in [postcard, birthcard, weddingcard]:
		print(card)

"""
OUTPUT:
(Jim <- Hello - Lee)
(Mark <- Happy birthday! - Bill)
(Lucy <- Happy forever! - Phoebe)
"""



