from helper_func import find

#Chemsynth Exception
class ChemsynthException(Exception): pass
class UnspecifiedColor(ChemsynthException): pass
class UnidentifiedColor(ChemsynthException): pass

class Chemsynth:
	'''
	+--------------------------------------------------------------------+
	|This Class provide almost tools needed for making Synthetic Chemical|
	|Solvent                [Disable]  *due to randomable rightmost color|
	|Replicator             [Enable]                                     |
	|Catalyst               [Enable]                                     |
	|Stirrer                [Enable]                                     |
	|Centrifuge             [Enable]                                     |
	+--------------------------------------------------------------------+
	+---------------------------------------------------------------+
	|Solvent                                                        |
	|chem = Chemsynth('RYPBG')                                      |
	|chem.solvent(0)                             #solvent at index 0|
	|chem.dom == [Y', 'P', 'B', 'G', '?']                           |
	+---------------------------------------------------------------+
	+---------------------------------------------------------------+
	|Replicator                                                     |
	|chem = Chemsynth('RYPBG')                                      |
	|chem.replicator(2)                       #replicator at index 2|
	|chem.dom == ['R', 'Y', 'P', 'P', 'B']                          |
	+---------------------------------------------------------------+
	+---------------------------------------------------------------+
	|Catalyst                                                       |
	|chem = Chemsynth('YYPBG')                                      |
	|chem.catalyst(0)                           #catalyst at index 0|
	|chem.dom == ['G', 'G', 'P', 'B', 'G']				|
	+---------------------------------------------------------------+
	+---------------------------------------------------------------+
	|Stirrer                                                        |
	|chem = Chemsynth('YYPBG')                                      |
	|chem.stirrer(2)                             #stirrer at index 2|
	|chem.dom == ['Y', 'B', 'P', 'Y', 'G']                          |
	+---------------------------------------------------------------+
	+---------------------------------------------------------------+
	|Centrifuge                                                     |
	|chem = Chemsynth('YYPBG')                                      |
	|chem.centrifuge(2)                       #centrifuge at index 2|
	|chem.dom == ['G', 'B', 'P', 'Y', 'Y']                          |
	+---------------------------------------------------------------+
	'''

	#######################################################################################
	#####################################Class Member######################################
	#######################################################################################
	#list of expected input color string
	color_table = ('R', 'Y', 'G', 'B', 'P', 'R')

	#######################################################################################
	################################Class Building Function################################
	#######################################################################################
	def __init__(self, dom):
		#validating input color
		self.__color_validation(dom)

		#initialization
		self.dom = list(dom.upper().strip()) 

	def __repr__(self):
		return "[" + "|".join(self.dom) + "]"

	def get_dom(self):
		'''
		attribute fetching for dom required if you want to make new instance from
		another instance's dom
		'''
		return ''.join(self.dom)

	#######################################################################################
	###################################Interface Helper####################################
	#######################################################################################
	@staticmethod
	def __color_validation(color_string):
		'''
		validating input color based on Chemsynth.color_table
		'''
		#prepare
		temp = color_string.upper().strip()

		#test for empty color
		if temp == "":
			raise UnspecifiedColor("color not specified")

		#test for unidentified color
		for index in range(len(temp)):
			if not(temp[index] in Chemsynth.color_table):
				raise UnidentifiedColor("unidentified color: '%s'" % (color_string[index]))

	@staticmethod
	def __centrifuge_far(length, index):
		'''
		produce a maximum block distance that can be affected by a centrifuge
		'''
		mid = length >> 1						#length // 2
		max_value = (mid) - ((length & 1)^1)	#length % 2 == length & 1

		if index > mid:							#upper than mid
			return max_value - index + mid
		elif index == mid:						#mid
			return max_value
		return index							#lower than mid

	@staticmethod
	def __catalyst_range(tank, index):
		'''
		produce a maximum block range that can be affected by a catalyst
		'''
		x, y = index, index
		#calculating start index
		while x-1 > -1 and tank[x-1] == tank[index]:
			x -= 1
		#calculating end index
		while y+1 < len(tank) and tank[y+1] == tank[index]:
			y += 1

		return (x, y+1)		#return (start index, after end index)

	def __color_changer(self, index):
		'''
		this function changed the item color to the next color in color_table
		'''
		#get index of color based on color_table
		a = find(Chemsynth.color_table, self.dom[index])

		#change color to the next color
		self.dom[index] = Chemsynth.color_table[a+1]

	#######################################################################################
	#######################################Interface#######################################
	#######################################################################################
	def solvent(self):		#undefined due to randomable rightmost element
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
		#shifting block to the right start at index till len-1 but
		#doing from right
		for i in range(len(self.dom)-1, index, -1):
			self.dom[i] = self.dom[i-1]

	def catalyst(self, index):
		'''
		Use on a highlighted Chemsynth Tank to shift its color
		upward on the spectrum (Red, Yellow, Green, Blue,
		Pink, Red). This also affects all touching tanks of the
		same color.
		'''
		#get range start from x, end at y (excluding y)
		x, y = self.__catalyst_range(self.dom, index)
		#change color to the next color
		self.__color_changer(index)
		#side effect of catalyst, affect all the same color before
		#color changed
		for i in range(x, y):
			self.dom[i] = self.dom[index]

	def stirrer(self, index):
		'''
		Use on a highlighted Chemsynth Tank to swap the
		chemicals on either side of it with each other. The
		selected tank is unaffected.
		'''
		#out of range mitigation
		if not(index == 0 or index == len(self.dom)-1):
			#swap color
			self.dom[index-1], self.dom[index+1] =  self.dom[index+1], self.dom[index-1]

	def centrifuge(self, index):
		'''
		Use on a highlighted Chemsynth Tank to rotate 
		chemicals around it. Rotates as many from the right
		as it can to match how many are to the left of the
		selected tank.
		'''
		#get the maximum distance that can be reached by centrifuge
		range_plus_or_minus = self.__centrifuge_far(len(self.dom), index)
		#swap color
		for x in range(1, range_plus_or_minus+1):
			self.dom[index-x], self.dom[index+x] =  self.dom[index+x], self.dom[index-x]