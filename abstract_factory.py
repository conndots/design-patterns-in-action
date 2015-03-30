import random

#factory classes
class BikeFactory:
	def get_vehicle(self):
		return Bike()

class CarFactory:
	def get_vehicle(self):
		return Car()

#concrete products
class Bike(object):
	def transport(self, target, from_where, to_where):
		print("Transport {} from {} to {} by Bike.".format(target, from_where, to_where))

class Car(object):
	def transport(self, target, from_where, to_where):
		print("Transport {} from {} to {} by Car.".format(target, from_where, to_where))

def get_random_factory():
	return random.choice([CarFactory, BikeFactory])()

#client
class Mike(object):
	def __init__(self, vehicle_factory=None):
		self.vehicle_factory = vehicle_factory

	def transport(self, from_where, to_where):
		vehicle = self.vehicle_factory.get_vehicle()
		vehicle.transport(self, from_where, to_where)

	def __str__(self):
		return "Mike"

if __name__ == "__main__":
	for i in range(10):
		mike = Mike(get_random_factory())
		mike.transport("Home", "Company")
		print("=" * 20)

### OUTPUT ###
#Transport Mike from Home to Company by Car.
#====================
#Transport Mike from Home to Company by Car.
#====================
#Transport Mike from Home to Company by Bike.
#====================
#Transport Mike from Home to Company by Car.
#====================
#Transport Mike from Home to Company by Bike.
#====================
#Transport Mike from Home to Company by Car.
#====================
#Transport Mike from Home to Company by Car.
#====================
#Transport Mike from Home to Company by Bike.
#====================
#Transport Mike from Home to Company by Car.
#====================
#Transport Mike from Home to Company by Bike.
#====================