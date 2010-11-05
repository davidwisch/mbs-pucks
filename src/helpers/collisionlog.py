"""
Keeps a two-way log of collisions between pucks in a
particular timestap.  Helps reduce the puck clustering problem
as well and removes the double collision problem.

Double Collision Problem:
Puck A detects collision with Puck B, calculates new velocities and updates
both.  Further in the loop, Puck B retetects a collision with Puck A and
repeats the calculations from earlier.  This is not only inefficient, but
also logically incorrect since the evolution functions updates both pucks
upon detecting the collision.

Author: David Wischhusen
"""

"""
Collision Log Class
"""
class CollisionLog:
	def __init__(self):
		self.puck_1_list = []
		self.puck_2_list = []

	def log_collision(self, puck1, puck2):
		p1name = puck1.get_name()
		p2name = puck2.get_name()

		self.puck_1_list.append(p1name)
		self.puck_2_list.append(p2name)

	def has_collided(self, puck1, puck2):
		p1name = puck1.get_name()
		p2name = puck2.get_name()

		for i in range(len(self.puck_1_list)):
			if self.puck_1_list[i] == p1name:
				if self.puck_2_list[i] == p2name:
					return True
			if self.puck_2_list[i] == p1name:
				if self.puck_1_list[i] == p2name:
					return True

		return False

	def clear_log(self):
		self.puck_1_list = []
		self.puck_2_list = []

	def __str__(self):
		out_str = '['
		for i in range(len(self.puck_1_list)):
			out_str += "(%s <==> %s), " % (
				self.puck_1_list[i],
				self.puck_2_list[i]
				)

		return out_str + ']'
