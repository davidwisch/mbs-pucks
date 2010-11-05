"""
Collection of various functions to cleanup the file structure
before or after a simulation.

Author: David Wischhusen
"""

import os
import shutil
import re

import settings
from . import general

"""
Clears the output directory of any files from previous runs
"""
def clear_output():
	print("Cleaning up output folder...")
	out_dir = general.get_path(settings.OUTPUT_DIRECTORY)

	#delete the output folder
	files = general.list_folder(out_dir)
	for f in files:
		os.unlink(f)

"""
Clears the pyc files at the end of a run.
This is done for cosmetic reasons only, I was sick of these files mucking
up my directories.
"""
def clear_pyc():
	print("Clearing *.pyc files...")

	regex = re.compile(r"\.pyc$")
	basepath = general.get_path()
	files = general.list_folder(basepath)

	for f in files:
		match = regex.search(f)
		if match:
			os.unlink(f)
