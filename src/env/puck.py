"""
The Puck object is the representation of a single puck on the table.
It's properties extend Obj.

Author: David Wischhusen
"""


import settings

from .obj import Obj
from helpers.position import Position
from helpers.velocity import Velocity

class Puck(Obj):
	def __init__(self, name = False, x_pos = False, y_pos = False, radius = False):
		Obj.__init__(self, name)

		self.position = Position(float(x_pos), float(y_pos))
		self.velocity = Velocity(0.0, 0.0)

		self.radius = radius if radius else settings.PUCK_RADIUS

		self.mass = settings.PUCK_MASS

	def get_mass(self):
		return self.mass

	def set_mass(self, mass):
		self.mass = mass

	def get_position(self):
		return self.position

	def set_position(self, position):
		self.position = position

	def get_x(self):
		return self.position.get_x()

	def set_x(self, x_pos):
		self.position.set_x(float(x_pos))

	def get_y(self):
		return self.position.get_y();

	def set_y(self, y_pos):
		self.position.set_y(float(y_pos))

	def	get_radius(self):
		return self.radius

	def set_radius(self, radius):
		self.radius = float(radius)

	def get_velocity(self):
		return self.velocity

	def set_velocity(self, velocity):
		self.velocity = velocity

	def get_vx(self):
		return self.velocity.get_x()

	def set_vx(self, vx):
		self.velocity.set_x(float(vx))

	def get_vy(self):
		return self.velocity.get_y();

	def set_vy(self, vy):
		self.velocity.set_y(float(vy))

	def __str__(self):
		return "Puck: %s at (%s, %s) going (%s, %s)" % (
			self.get_name(),
			self.get_x(),
			self.get_y(),
			self.get_vx(),
			self.get_vy()
			)
