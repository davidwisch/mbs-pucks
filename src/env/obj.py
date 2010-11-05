"""
General object class the other classes in this package inherit.

Author: David Wischhusen
"""


"""
Object class
"""
class Obj:
	def __init__(self, name = False):
		self.name = name

	def get_name(self):
		return self.name

	def set_name(self, name):
		self.name = name

	def __str__(self):
		return self.name
