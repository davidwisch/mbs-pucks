"""
Class that keeps track of the bin distribution of pucks at a particular timestep
"""
class Distribution:
	def __init__(self):
		self.bins = [0]*30 #30 bins, more than we'll need, they get filtered out

	def increment_bin(self, binno):
		self.bins[binno] += 1

	def get_bins(self):
		return self.bins
