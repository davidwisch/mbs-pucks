"""
General class that represents a 2D velocity in cartesian coordinates.

Author: David Wischhusen
"""

class Velocity:
	def __init__(self, x = False, y = False):
		self.x_component = float(x)
		self.y_component = float(y)

	def get_x(self):
		return self.x_component

	def set_x(self, x):
		self.x_component = float(x)

	def get_y(self):
		return self.y_component

	def set_y(self, y):
		self.y_component = float(y)

	def __str__(self):
		return "Vel: (%s, %s)" % (self.x_component, self.y_component)
