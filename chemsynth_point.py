from chemsynth import *

class Chemsynth_point(object):
	'''
	This Class provide the point of tool to selected tank
	'''
	def __init__(self, dom, tar):
		self.dom = dom
		self.tar = tar

	@staticmethod
	def __point1(list1, list2): 		#this function return point for stirrer point and replicator point
		value = 0
		for i in range(len(list1)):
        		if list1[i] == list2[i]:
      	  			value += 1
		return value

	@staticmethod
	def __point2(list1, list2): 		#return point for centrifuge point
		value = 0
		length = len(list1)
		half = length//2
		for i in range(half):
			if list1[i] == list2[i]:
				value += half-i
		for i in range(half, length):
			if list1[i] == list2[i]:
				value += i-1
		return value
	
	@staticmethod
	def __catalyst_range(tank, index):
		x,y,z = index, index, 1
		index_temp = index - 1
		while (index_temp >= 0 and index_temp < len(tank)) and (tank[index_temp] == tank[index]):
			index_temp -= 1
			x -= 1
			z += 1
		index_temp = index + 1
		while (index_temp < len(tank)) and (tank[index_temp] == tank[index]):
			index_temp += 1
			y += 1
			z += 1
		return (x,y+1,z)

	@staticmethod
	def __centrifuge_help(list1, list2, index, n):
		x = 0
		for i in range(-n, 0):
			list1[x] = list2[index+i]
			x += 1
		for i in range(1, n+1):
			list1[x] = list2[index+i]
			x += 1

	def replicator_point(self, index):		#return the point of replicator on selected tank
		length = len(self.dom)
		temp = Chemsynth(list(self.dom))
		block_changed = length-1-index
		old_block = [0]*block_changed
		target_block = [0]*block_changed
		new_block = [0]*block_changed
		copy(old_block, self.dom, index+1, length)
		copy(target_block, self.tar, index+1, length)
		temp.replicator(index)
		copy(new_block, temp.dom, index+1, length)

		return self.__point1(new_block, target_block) - self.__point1(old_block, target_block)

	def catalyst_point(self, index):		#return the point of catalyst on selected tank
		x,y,block_changed = self.__catalyst_range(self.dom, index)
		temp = Chemsynth(list(self.dom))
		old_block = [0]*block_changed
		target_block = [0]*block_changed
		new_block = [0]*block_changed

		copy(old_block, self.dom, x, y)
		copy(target_block, self.tar, x, y)
		temp.catalyst(index)
		copy(new_block, temp.dom, x, y)
	
		return self.__point1(new_block, target_block) - self.__point1(old_block, target_block)

	def stirrer_point(self, index):			#return the point of stirrer on selected tank
		if (index == 0) or (index == len(self.dom)-1):
			return 0
		temp = Chemsynth(list(self.dom))
		old_block = (self.dom[index-1], self.dom[index+1])
		target_block = (self.tar[index-1], self.tar[index+1])
		temp.stirrer(index)
		new_block = (temp.dom[index-1], temp.dom[index+1])
		
		return self.__point1(new_block, target_block) - self.__point1(old_block, target_block)

	def centrifuge_point(self, index):		#return the point of centrifuge on selected tank
		block_changed = range_max(self.dom,index)*2
		old_block = [0]*block_changed
		target_block = [0]*block_changed
		new_block = [0]*block_changed
		temp = Chemsynth(list(self.dom))
		self.__centrifuge_help(old_block, self.dom, index, block_changed//2)
		self.__centrifuge_help(target_block, self.tar, index, block_changed//2)
		temp.centrifuge(index)
		self.__centrifuge_help(new_block, temp.dom, index, block_changed//2)
	
		return self.__point2(new_block, target_block) - self.__point2(old_block, target_block)