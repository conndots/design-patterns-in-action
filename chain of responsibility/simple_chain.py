"""
chain of responsibility pattern:
Avoid coupling the sender of a request to its receiver by giving more than one object a chance to handle the request. Chain the receiving objects and pass the request along the chain until an object handles it.
"""
class Handler:
	def __init__(self, successor=None):
		self._successor = successor

	def handle_request(self, request):
		response = self._handle(request)
		if not response and self._successor:
			response = self._successor._handle(request)
		if not response:
			raise Exception("Cannot handle the request ({}).".format(request))
		return response

class HundredsHandler(Handler):
	def _handle(self, request):
		if request < 1000 and request >= 0:
			print('Handle ({}) by {}'.format(request, self.__class__.__name__))
			return 2
		return False

class ThounsandsHandler(Handler):
	def _handle(self, request):
		if request < 10000 and request >= 1000:
			print('Handle ({}) by {}'.format(request, self.__class__.__name__))
			return 3
		return False

def get_chained_handler():
	return HundredsHandler(ThounsandsHandler())

def main():
	handler = get_chained_handler()
	requests = [100, 300, 500, 10, 5000, 9000, 1000, 100000]
	for r in requests:
		try:
			print("response: {}".format(handler.handle_request(r)))
		except Exception as e:
			print('{}'.format(e))

if __name__ == '__main__':
	main()

"""
OUTPUT:
Handle (100) by HundredsHandler
response: 2
Handle (300) by HundredsHandler
response: 2
Handle (500) by HundredsHandler
response: 2
Handle (10) by HundredsHandler
response: 2
Handle (5000) by ThounsandsHandler
response: 3
Handle (9000) by ThounsandsHandler
response: 3
Handle (1000) by ThounsandsHandler
response: 3
Cannot handle the request (100000).
"""
