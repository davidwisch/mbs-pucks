import os
import math

import settings
import stats

from helpers import general
from statistics.dfo import DFO

"""
Generate the distributions of pucks within the bins on the table.
The name suggusts that this is an average but its not really.
"""
def average_distributions(distributions):
	avg_dist = [0]*len(distributions[0].get_bins())
	for ts in range(len(distributions)):
		for binno in range(len(distributions[ts].get_bins())):
			value = distributions[ts].get_bins()[binno]
			avg_dist[binno] += value
	return avg_dist

"""
Take the distribution of pucks of output them to an image
"""
def distributions_snapshot(gigafile_name):
	from pylab import scatter, show, xlim, ylim, clf, savefig, title, xlabel, ylabel

	print "Outputting Average Distribution Snapshot"

	dfo = DFO(os.path.join(general.get_path(settings.OUTPUT_DIRECTORY), gigafile_name))

	distributions = []
	for ts in range(dfo.num_timesteps()):
		distributions.append(dfo.get_timestep(ts).get_distribution())

	avg_distribution = stats.average_distributions(distributions)

	x_vals = []
	y_vals = []

	for i in range(len(avg_distribution)):
		if avg_distribution[i] == 0: continue
		x_vals.append(i)
		y_vals.append(math.log(avg_distribution[i]))

	title("Bin Counts")
	xlabel("Bin")
	ylabel("Count")
	scatter(x_vals, y_vals)
	savefig(os.path.join(general.get_path(settings.OUTPUT_DIRECTORY), "distribution.png"))

"""
Take the distribution of pucks accross all timestamps and turns them into a heatmap
"""	
def heatmap(gigafile_name):
	import numpy
	
	dfo = DFO(os.path.join(general.get_path(settings.OUTPUT_DIRECTORY), gigafile_name))

	DIMX = 50
	DIMY = 50
	dx = dfo.get_timestep(0).get_table().get_width() / DIMX
	dy = dfo.get_timestep(0).get_table().get_height() / DIMY
	grid = numpy.zeros((DIMX, DIMY), "float32")
	for ts in range(dfo.num_timesteps()):
		pucks = dfo.get_timestep(ts).get_table().get_pucks()
		for puck in pucks:
			x,y = puck.get_x(), puck.get_y()
			bin_x = int(x / dx)
			bin_y = int(y / dy)
			grid[bin_x, bin_y] += 1
	dat_file = open(os.path.join("..", 'output', "datfile.txt"), "w")
	for x in range(grid.shape[0]):
		for y in range(grid.shape[1]):
			dat_file.write("%s %s %s\n" % (x * dx, y * dy, grid[x, y]))
		dat_file.write("\n")
	dat_file.close()
	
	#output gnuplot config file
	config = open(os.path.join("..", "output", "gnuplot.config"), "w")
	config.write("set view map\n")
	config.write("set contour base\n")
	config.write("set output '%s'\n" % (os.path.join("..", "output", "heatmap.png")))
	config.write("set term png\n")
	config.write("splot '%s' w pm3d\n" % (os.path.join("..", "output", "datfile.txt")))
	config.write("set terminal windows\n")
	config.close()
	os.system("%s %s" % (settings.GNUPLOT_COMMAND, os.path.join("..", "output", "gnuplot.config")))
	
