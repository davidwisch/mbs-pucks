"""
The Timestep object contains a Table instance at a certain timestep.
Class contains statistical functions that can be applied to the table
either directly or by the containing DFO object.
"""
import settings

from statistics.distribution import Distribution
from helpers.position import Position
from helpers.velocity import Velocity

class Timestep:
	def __init__(self, table):
		self.table = table
		self.name = self.table.get_name()

	def get_table(self):
		return self.table

	def get_name(self):
		return self.name

	def average_position(self):
		x_vals = 0.0
		y_vals = 0.0

		for puck in self.table.get_pucks():
			x_vals += puck.get_x()
			y_vals += puck.get_y()
		x_vals /= self.table.num_pucks()
		y_vals /= self.table.num_pucks()

		return Position(x_vals, y_vals)

	def average_velocity(self):
		x_vel = 0.0
		y_vel = 0.0

		for puck in self.table.get_pucks():
			x_vel += puck.get_vx()
			y_vel += puck.get_vy()
		x_vel /= self.table.num_pucks()
		y_vel /= self.table.num_pucks()

		return Velocity(x_vel, y_vel)

	def get_distribution(self):
		dist = Distribution()
		for puck in self.table.get_pucks():
			y_pos = puck.get_y()
			bin = int(y_pos % (settings.BIN_SPACING * 2.0))
			dist.increment_bin(bin)
		return dist

	def __str__(self):
		return "Timestep: %s" % (self.name)
