from helper_func import *

class Chemsynth(object):
	'''
	This Class provide all tools needed for making Synthetic Chemical
	'''
	def __init__(self, dom):
		self.dom = dom

	def solvent(self):		#undefined due randomable rightmost element
		pass
		'''
		Use on a highlighted Chemsynth Tank to dissolve it,
		shifting chemicals left to fill in the gap. A random
		chemical is added in the rightmost tank.
		'''

	def replicator(self, index):
		'''
		Use on a highlighted Chemsynth Tank to duplicate its
		content, pushing all chemicals to the right to make
		room.
		'''
		last_index = len(self.dom)-1
		for i in range(last_index,index,-1):
			self.dom[i] = self.dom[i-1]
	
	def catalyst(self, index):
		'''
		Use on a highlighted Chemsynth Tank to shift its color
		upward on the spectrum (Red, Yellow, Green, Blue,
		Pink, Red). This also affects all touching tanks of the
		same color.
		'''
		old = self.dom[index]
		color_changer(self.dom,index)
		index_temp = index + 1
		while (index_temp < len(self.dom)) and (self.dom[index_temp] == old):
			self.dom[index_temp] = self.dom[index]
			index_temp += 1
		index_temp = index - 1
		while (index_temp >= 0 and index_temp < len(self.dom)) and (self.dom[index_temp] == old):
			self.dom[index_temp] = self.dom[index]
			index_temp -= 1

	def stirrer(self, index):
		'''
		Use on a highlighted Chemsynth Tank to swap the
		chemicals on either side of it with each other. The
		selected tank is unaffected.
		'''
		if (index == 0) or (index == len(self.dom)-1):
			return
		temp = self.dom[index+1]
		self.dom[index+1] = self.dom[index-1]
		self.dom[index-1] = temp

	def centrifuge(self, index):
		'''
		Use on a highlighted Chemsynth Tank to rotate 
		chemicals around it. Rotates as many from the right
		as it can to match how many are to the left of the
		selected tank.
		'''
		range_plus_or_minus = range_max(self.dom,index)
		for x in range(1,range_plus_or_minus+1):
			temp = self.dom[index+x]
			self.dom[index+x] = self.dom[index-x]
			self.dom[index-x] = temp
