"""
Parses and stores the command line options that the simulation accepts.

Author: David Wischhusen
"""

from optparse import OptionParser

def parse():
	print "Loading Option Parser....."

	parser = OptionParser()
	parser.add_option('-c', '--no-check', dest='check_deps',
					help="don't check dependencies",
					action="store_false",
					default=True)
	parser.add_option('-d', '--dirty-mode', dest='clear_compiled',
					help="don't clear .pyc files",
					action="store_false",
					default=True)
	parser.add_option('-i', '--images', dest='to_images',
					help="output to images",
					action="store_true",
					default=False)
	parser.add_option('-f', '--files', dest='to_files',
					help="output to files",
					action="store_true",
					default=False)
	parser.add_option('-g', '--gigafile', dest='gigafile',
					help="output to one file",
					action="store_true",
					default=False)

	options, args = parser.parse_args()

	return options
