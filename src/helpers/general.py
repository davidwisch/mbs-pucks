"""
Contains general functions that may be of assistance at times.

Author: David Wischhusen
"""

import sys
import os

import settings

"""
Gets the alsolute path to a given path relative to the simulation script
"""
def get_path(dirname=False):
	basepath = os.path.abspath(os.path.dirname(sys.argv[0]))
	if not dirname:
		return basepath

	return os.path.join(basepath, dirname)

"""
Recursivly list the contents of a directory
"""
def list_folder(dirname):
	fileList = []
	for root, subFolders, files in os.walk(dirname):
		for file in files:
			fileList.append(os.path.join(root,file))

	return fileList

def match_sign(num1, num2):
	if num1 * num2 < 0:
		return False
	return True
