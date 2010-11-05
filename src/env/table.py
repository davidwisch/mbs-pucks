"""
Table object represents the table on which all the pucks are contained.
Extends Obj.  Contains functions to output its current state in various
different formats (files, images, gigafile).

Author: David Wischhusen
"""

import settings

from .obj import Obj
from helpers import general

"""
Table Class
"""
class Table(Obj):
	def __init__(self, name = False, width = False, height = False, slant = False):
		Obj.__init__(self, name)

		#initialize with custom or set to default
		self.width = float(width) if width else settings.TABLE_WIDTH
		self.height = float(height) if height else settings.TABLE_HEIGHT
		self.slant = float(slant) if slant else settings.TABLE_SLANT

		self.pucks = []

		self.GIGAFILE_NAME = "gigadump.txt"

	def get_width(self):
		return self.width

	def set_width(self, width):
		self.width = float(width)

	def get_height(self):
		return self.height

	def set_height(self, height):
		self.height = float(height)

	#should be expressed in degrees
	def get_slant(self):
		return self.slant

	#should be expressed in degrees
	def set_slant(self, slant):
		self.slant = float(slant)

	def get_pucks(self):
		return self.pucks

	def set_puck(self, puck):
		self.pucks.append(puck)

	def num_pucks(self):
		return len(self.pucks)

	#output the current state of the table to a datafile in the output directory
	def file_snapshot(self, timestep):
		import os

		output = os.path.join(general.get_path(settings.OUTPUT_DIRECTORY), "ts_%s.txt" % (timestep))
		snapshot = open(output, 'w')
		for puck in self.pucks:
			name= puck.get_name()
			xx = puck.get_x()
			xy = puck.get_y()
			vx = puck.get_vx()
			vy = puck.get_vy()

			snapshot.write("%s %s %s %s %s\n" % (name, xx, xy, vx, vy))
		snapshot.close()

	#output the current state of the table into a graph and save in the output dir
	def snapshot(self, timestep, to_screen = False):
		from pylab import scatter, show, xlim, ylim, clf, savefig, title, xlabel, ylabel
		import os

		x_vals = []
		y_vals = []

		for p in self.pucks:
			x_vals.append(p.get_x())
			y_vals.append(p.get_y())

		#if we don't clear, things build up in the buffer and we get
		#magic spawning pucks - this buffer must exist in the global namespace
		clf()

		title("Puck Positions (pucks not to scale)")
		xlabel("Table Width")
		ylabel("Table Height")
		scatter(x_vals, y_vals,s=710.0)
		xlim( (0, settings.TABLE_WIDTH) )
		ylim( (0, settings.TABLE_HEIGHT) )
		savefig(os.path.join(general.get_path(settings.OUTPUT_DIRECTORY), "ts_%s.png" % (timestep)))

		if to_screen:
			show()

	#output the current timestap into an appended file.  All timesteps will be stored in one file
	def gigasnap(self, timestep):
		import os
		#We should save time by maintaining the file file connection rather than doing open/close w/ append - pretty significant
		#We'll also lose speed going try/catch - but according to my benchmarks, almost none
		try:
			self.gigafile
		except(AttributeError):
			self.gigafile = open(os.path.join(general.get_path(settings.OUTPUT_DIRECTORY), self.GIGAFILE_NAME), 'w')

		self.gigafile.write("#Timestep: %s\n" % (timestep))
		for puck in self.pucks:
			output_str = "%s %s %s %s %s" % (
				puck.get_name(),
				puck.get_x(),
				puck.get_y(),
				puck.get_vx(),
				puck.get_vy()
			)
			self.gigafile.write("%s\n" % (output_str))
		self.gigafile.write("\n") #separate this timestep from the next

		#we'll let the file connection die with the process

	def __str__(self):
		return "Table: %s" % self.get_name();
