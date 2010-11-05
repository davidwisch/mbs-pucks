"""
General class representing a 2D position in cartesian coordinates.

Author: David Wischhusen
"""
class Position:
	def __init__(self, x = False, y = False):
		self.x_position = float(x)
		self.y_position = float(y)

	def get_x(self):
		return self.x_position

	def set_x(self, x):
		self.x_position = float(x)

	def get_y(self):
		return self.y_position

	def set_y(self, y):
		self.y_position = float(y)

	def __str__(self):
		return "Pos: (%s, %s)" % (self.x_position, self.y_position)
