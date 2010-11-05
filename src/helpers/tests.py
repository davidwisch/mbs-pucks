"""
Dependency checker to make sure we have all of the modules, etc that
we need for all of the functions possible in the simulation.

Author: David Wischhusen
"""

def check_dependencies():
	print("Checking dependencies....")
	import sys
	all_clear = True

	deps = ([
		"pylab", "http://matplotlib.sourceforge.net/",
		"numpy", "http://numpy.scipy.org/"
		])

	for i in range(0, len(deps), 2):
		sys.stdout.write(("Checking presence of '%s'......" % deps[i]))
		try:
			exec("import %s" % deps[i])
			print "Passed."
		except(ImportError):
			all_clear = False
			print "FAILED."
			print "\t-Download at: '%s'" % (deps[i+1])

	if not all_clear:
		return "There were unmet dependencies.....exiting."

	return True
