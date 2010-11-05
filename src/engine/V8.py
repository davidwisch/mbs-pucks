"""
This is the actual engine, evolved by the simulation controller but
responsible for calling all of the appropriate physics functions to
evolve the pucks, detect collisions, etc.  Also contains puck spawning
function, etc.

Author: David Wischhusen
"""

import random
import math

from env.puck import Puck
from helpers.velocity import Velocity
from helpers.collisionlog import CollisionLog
from .engine import physics

"""
This is the Engine Object
"""
class V8:
	def __init__(self):
		pass

	def get_table(self):
		return self.table

	def set_table(self, table):
		self.table = table

	def get_timestep(self):
		return self.timestep

	def set_timestep(self, timestep):
		self.timestep = float(timestep)

	def can_place(self, candidate_puck):
		pucks = self.get_table().get_pucks()
		table = self.get_table()

		#check that the puck isn't overlapping the walls at all
		radius = candidate_puck.get_radius()

		#check top, cna only go 1/2 way up the table
		if candidate_puck.get_y() + radius > table.get_height() * 0.3:
			return False
		#check right
		if candidate_puck.get_x() + radius > table.get_width():
			return False
		#check bottom
		if candidate_puck.get_y() - radius < 0:
			return False
		#check left
		if candidate_puck.get_x() - radius < 0:
			return False

		if not len(pucks):
			return True

		cx = candidate_puck.get_x()
		cy = candidate_puck.get_y()

		for puck in pucks:
			px = puck.get_x()
			py = puck.get_y()

			dx = abs(cx - px)
			dy = abs(cy - py)

			dist = math.sqrt(dx**2 + dy**2)

			if dist < candidate_puck.get_radius() + puck.get_radius():
				return False
		return True

	#puts a puck on the table
	def spawn_puck(self, velocity=False):
		table = self.get_table()

		candidate_x = random.random() * table.get_width()
		candidate_y = random.random() * table.get_height()

		p = Puck('candidate', candidate_x, candidate_y)
		while not self.can_place(p):
			candidate_x = random.random() * table.get_width()
			candidate_y = random.random() * table.get_height()

			p = Puck('candidate', candidate_x, candidate_y)
		if velocity:
			#-0.5 so that there's a chance they have a negative velocity
			p.set_velocity(Velocity(random.random()-0.5, random.random()-0.5))

		p.set_name(table.num_pucks()+1)
		table.set_puck(p)

	#allows for manual setting of pucks on the table, usefull for testing
	def place_puck(self, x, y, vx=False, vy=False):
		table = self.get_table()

		p = Puck('candidate', x, y)
		if not self.can_place(p):
			print "ERROR: manually setting puck, overlapping pucks"
			return

		p.set_vx(vx)
		p.set_vy(vy)
		p.set_name(table.num_pucks()+1)
		table.set_puck(p)

	#Moves the pucks forward 1 timestep
	def evolve(self):
		pucks = self.table.get_pucks()
		num_pucks = len(pucks)
		collision_log = CollisionLog()

		for i in range(num_pucks):
			future_puck = physics.evolve_puck(pucks[i], self.timestep)

			#check for collisions with the wall
			future_puck = physics.wall_collision(pucks[i].get_position(), future_puck, self.timestep)

			#check for collisions with other pucks
			future_puck = physics.puck_collision(future_puck, pucks, self.timestep, collision_log)

			pucks[i] = future_puck

	def __str__(self):
		return "Just call me Ferrari"
