"""
mediator pattern:
Define an object that encapsulates how a set of objects interact. Mediator promotes loose coupling by keeping
objects from refering to each other explicitly, and it lets you vary their interaction independently.

Here is an example of mediator pattern.
Reference: http://entitycrisis.blogspot.com/2007/07/mediator-pattern-in-python.html
A boy developer and his girlfriend are peer programming. One is coding and the other is doing peer reviewing 
and testing. A mediator handles the requests and handles between them.
A more sophisicated mediator should balance the requests to multiple handlers.
"""
import random

class Mediator:
	def __init__(self):
		self._handlers = {}

	def register_handler(self, service, handler):
		handlers = self._handlers.setdefault(service, [])
		handlers.append(handler)

	def unregister_handler(self, service, handler=None):
		if handler:
			handlers = self._handlers.get(service)
			if handlers:
				handlers.remove(handler)
		else:
			handlers.pop(service)

	def handle(self, service, *args, **kw):
		for handler in self._handlers.get(service, []):
			if hasattr(handler, service):
				return handler.__getattribute__(service)(*args, **kw)
			else:
				return handler(*args, **kw)

class BoyProgrammer:
	def __init__(self, mediator, *services):
		self._mediator = mediator
		for service in services:
			mediator.register_handler(service, self)

	def debug(self, code, f):
		print('The boy is debugging: {} from the request of {}'.format(code, f))
		return code.swapcase()

	def code(self):
		print('The boy is coding')
		return "CODE"

	def ask_to_review(self, code):
		print('The boy sends peer-reviewing request: {}'.format(code))
		return self._mediator.handle("peer_review", code)

	def ask_to_test(self, code):
		print('The boy sends QA test request: {} '.format(code))
		return self._mediator.handle("qa_test", code)

class GirlProgrammer:
	def __init__(self, mediator, *services):
		self._mediator = mediator
		for service in services:
			mediator.register_handler(service, self)

	def peer_review(self, code):
		print('This girl is peer-reviewing: {}'.format(code))
		if random.choice([True, False]): #0.5 possibility to detact bugs by reviewing code
			return self._mediator.handle('debug', code, 'peer_review')
		return code

	def qa_test(self, code):
		print('This girl is qa-testing: {}'.format(code))
		if random.choice([True, False]): #0.5 possibility to detact bugs by testing code
			return self._mediator.handle('debug', code, 'qa_test') 
		return code

def main():
	mediator = Mediator()
	boy = BoyProgrammer(mediator, "code", "debug")
	girl = GirlProgrammer(mediator, "peer_review", "qa_test")

	for i in range(5):
		code = boy.code()
		code = boy.ask_to_review(code)
		code = boy.ask_to_test(code)
		print("=" * 10)

if __name__ == '__main__':
	main()

"""
OUTPUT:
The boy is coding
The boy sends peer-reviewing request: CODE
This girl is peer-reviewing: CODE
The boy sends QA test request: CODE 
This girl is qa-testing: CODE
The boy is debugging: CODE from the request of qa_test
==========
The boy is coding
The boy sends peer-reviewing request: CODE
This girl is peer-reviewing: CODE
The boy is debugging: CODE from the request of peer_review
The boy sends QA test request: code 
This girl is qa-testing: code
==========
The boy is coding
The boy sends peer-reviewing request: CODE
This girl is peer-reviewing: CODE
The boy sends QA test request: CODE 
This girl is qa-testing: CODE
==========
The boy is coding
The boy sends peer-reviewing request: CODE
This girl is peer-reviewing: CODE
The boy sends QA test request: CODE 
This girl is qa-testing: CODE
The boy is debugging: CODE from the request of qa_test
==========
The boy is coding
The boy sends peer-reviewing request: CODE
This girl is peer-reviewing: CODE
The boy is debugging: CODE from the request of peer_review
The boy sends QA test request: code 
This girl is qa-testing: code
==========
"""
