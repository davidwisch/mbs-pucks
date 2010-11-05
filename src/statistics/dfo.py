"""
DFO stands for "data file object" and allows you to extract statistics
from a table at any timestep.  Reads in a gigafile and creates a table
instance filled with puck instances at every timestep.

Author: David Wischhusen
"""

import re
import os
import math

import settings

from env.table import Table
from env.puck import Puck
from statistics.timestep import Timestep


"""
DFO is the data file object, it contains timesteps.  Statistics actions
that are executed on the DFO automatically aggregate the same function
applied to its containing timesteps.
"""
class DFO:
	def __init__(self, gigafile=False):
		self.gigafile = gigafile
		file = open(self.gigafile)
		self.contents = file.read()
		file.close()
		self.parse()

	def gigafile(self):
		return self.gigafile

	def parse(self):
		timesteps = self.contents.split("\n\n")
		self.timesteps = []
		i=1
		for ts in timesteps:
			table = Table(i) #let the rest default
			lines = ts.split("\n")
			del lines[0] #get rid of the timestep label
			for line in lines:
				segments = line.split(" ")
				try:
					puck = Puck(
						segments[0],
						segments[1],
						segments[2],
					) #let radius default
					puck.set_vx(segments[3])
					puck.set_vy(segments[4])
				except:
					continue

				table.set_puck(puck)
			timestep_instance = Timestep(table)
			self.timesteps.append(timestep_instance)
			i += 1

	def num_timesteps(self):
		return len(self.timesteps)

	def get_timestep(self, timestep):
		return self.timesteps[timestep-1]
