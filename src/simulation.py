"""
Controller for the puck simulation.  Engine, pucks, table are created here.
There should not be any simulation logic in here.

Author: David Wischhusen
"""

import time
import sys
import traceback

import settings

from engine.V8 import V8
from env.table import Table
from helpers import cleanup
from helpers import tests
from helpers import cli
from statistics import stats


if __name__ == "__main__":
	#load our cli parser
	options = cli.parse()

	try:
		#run our startup tests
		if options.check_deps:
			results = tests.check_dependencies()
			if results != True:
				#we still want a clean file tree
				if options.clear_compiled:
					cleanup.clear_pyc()
				sys.exit(results)

		#run some cleanup functions
		cleanup.clear_output()

		#start the benchmark
		time_start = time.time()

		#create our engine
		engine = V8()

		#generate our table
		table = Table("Simulation Table")

		#populate our engine
		engine.set_table(table)
		engine.set_timestep(settings.TIMESTEP)

		#spawn pucks
		print "Spawning Pucks..."
		for i in range(settings.NUMBER_OF_PUCKS):
			engine.spawn_puck(velocity=True)

		#step our pucks
		print "Starting Simulation..."
		timesteps = settings.TIMESTEPS
		for i in range(timesteps):
			engine.evolve()
			if i % settings.OUTPUT_IMAGE_STEPS == 0:
				if options.to_images: #dump snapshot to an image
					engine.get_table().snapshot(i)
				if options.to_files: #dump snapshot to a txt file
					engine.get_table().file_snapshot(i)
				if options.gigafile: #dump all puck positions to one large output file
					engine.get_table().gigasnap(i)

		time_end = time.time()

		print "Simulation Complete.  Took:", time_end-time_start, "seconds"

		print "Performing Analysis..."
		if options.gigafile:
			stats.distributions_snapshot(engine.get_table().GIGAFILE_NAME)
			stats.heatmap(engine.get_table().GIGAFILE_NAME)
		print "Finished Permorming Analysis"

		#cleanup *.pyc files
		if options.clear_compiled:
			cleanup.clear_pyc()

	#EXCEPTION HANDLING
	except KeyboardInterrupt:
		print "\nKeyboard interrupt detected, cleaning up and exiting..."
		if options.clear_compiled:
			cleanup.clear_pyc()
	except:
		traceback.print_exc()
		if options.clear_compiled:
			cleanup.clear_pyc()
