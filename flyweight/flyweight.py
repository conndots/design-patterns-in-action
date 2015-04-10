"""
Flyweight pattern:
Use sharing to support large numbers of fine-grained objects efficiently.
This example comes from: http://codesnipers.com/?q=python-flyweights
"""

import weakref

class Card(object):
    __card_pool = weakref.WeakValueDictionary()

    def __new__(cls, value, suit):
        obj = Card.__card_pool.get(suit + str(value), None)
        if not obj:
            obj = object.__new__(cls)
            Card.__card_pool[suit + str(value)] = obj
            obj.value, obj.suit = value, suit

        return obj

    def __str__(self):
    	return "CARD:{}{}".format(self.value, self.suit)

def main():
	card_4H = Card(4, 'H')
	card_5C = Card(5, 'C')
	card_4H_ = Card(4, 'H')
	print(card_4H == card_4H_)
	print(card_5C)

if __name__ == '__main__':
	main()

"""
OUTPUT:
True
CARD:5C
"""