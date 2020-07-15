from chemsynth import Chemsynth, ChemsynthException
from helper_func import find, copy

__all__ = ['ChemsynthPoint']

# =========================
# Chemsynth Point Exception
# =========================

class ChemsynthPointException(ChemsynthException): pass
class ColorLengthError(ChemsynthPointException): pass

# =============================
# Utility functions and classes
# =============================

class ChemsynthPoint(Chemsynth):
	'''
	This Class provide the point of tool on selected tank
	'''

	# ========================
	# Class Building Functions
	# ========================

	def __init__(self, dom, tar):
		#validating input color
		self._Chemsynth__color_validation(dom)
		self._Chemsynth__color_validation(tar)
		if len(dom) != len(tar):
			raise ColorLengthError("inconsistent of colors length")

		#initialization
		self.dom = list(dom.upper().strip())
		self.tar = list(tar.upper().strip())

	def get_tar(self):
		'''
		attribute fetching for tar required if you want to make new instance from
		another instance's tar
		'''
		return ''.join(self.tar)

	# ================
	# Interface Helper
	# ================

	@staticmethod
	def __point1(list1, list2):
		'''
		return the same total items contained at the same index
		'''
		value = 0
		#calculating
		for index in range(len(list1)):
        		if list1[index] == list2[index]:
      	  			value += 1

		return value

	@staticmethod
	def __point2(list1, list2):
		'''
		this function is specific to centrifuge. basically it calculates
		like __point1 does, but the centrifuge has various distances,
		so the longer a list the bigger the points obtained. 
		'''
		value = 0
		length = len(list1)
		half = 	length >> 1		#value // 2 == value >> 1
		#calculating
		for index in range(length):
			if index < half:
				value += half - index
			else:
				value += index - half + 1

		return value

	@staticmethod
	def __centrifuge_copy(list1, list2, index, n):
		'''
		this function is specific to centrifuge copy. basically copy items from list2 to list1,
		but there are differences from just copying it. This function copies items from
		index - n until index + n + 1, does not include items at the index; from list2 to list1.
		'''
		x = 0
		for i in range(index-n, index+n+1):
			if i == index:
				continue
			list1[x] = list2[i]
			x += 1

	@staticmethod
	def __color_distance(color_dom, color_tar):
		'''
		This function calculates the distance of two colors based on Chemsynth.color_table
		'''
		#getting index color
		dom_value = find(Chemsynth.color_table, color_dom)
		tar_value = find(Chemsynth.color_table, color_tar)

		#calculating
		if dom_value <= tar_value:
			return tar_value - dom_value 
		return 5 - dom_value + tar_value
		

	@staticmethod
	def __general_bonus(old_block, target_block, new_block):
		'''
		calculates the total distance of each color in a list against the colors in another
		list with the same index. return the bonus, bonuses based on the total distance of
		each color, then determined whether it makes it easy or vice versa.
		'''
		#prepare
		x, y = 0, 0
		length = len(old_block)

		#calculating
		for i in range(length):	
			x += ChemsynthPoint.__color_distance(old_block[i], target_block[i])
			if old_block[i] == target_block[i]:	#if old == target, it shouldn't move
				x -= 1
		for i in range(length):
			y += ChemsynthPoint.__color_distance(new_block[i], target_block[i])

		return x-y

	def __point_side(self, index, direction, temp):
		'''
		calculate the points specifically for the catalyst of the block on the right or left based on
		the direction. if direction == -1 then left, if direction == 1 then right.
		'''
		bonus = 0
		#out of range mitigation
		if (direction == 1 and index == len(self.dom)-1) or (direction == -1 and index == 0):
			return bonus

		#calculating
		if self.dom[index] == self.tar[index]:
			bonus = -1
		if (self.dom[index] != self.tar[index] and
                   self.dom[index] == self.dom[index+direction] and
                   self.dom[index+direction] == self.tar[index+direction]):
			bonus += -1

		if (temp.dom[index] != self.tar[index] and
                   self.dom[index+direction] == self.tar[index+direction] and
                   temp.dom[index] == self.dom[index+direction]):
			bonus += -1

		if self.dom[index] == self.dom[index+direction] and self.tar[index] == self.tar[index+direction]:
			bonus += 1

		if self.dom[index] != self.dom[index+direction] and self.dom[index] != self.tar[index]:
			bonus += 1

		return bonus

	# =========
	# Interface
	# =========

	def solvent_point(self, index):
		pass

	def replicator_point(self, index):
		'''
		return the point of replicator on selected tank
		'''
		#prepare
		length = len(self.dom)
		temp = Chemsynth(self.get_dom())
		block_changed = length-1-index

		#allocating enough space
		old_block = [0]*block_changed
		target_block = [0]*block_changed
		new_block = [0]*block_changed

		#filling the block
		copy(old_block, self.dom, index+1, length)
		copy(target_block, self.tar, index+1, length)
		temp.replicator(index)
		copy(new_block, temp.dom, index+1, length)

		#calculating point
		bonus = self.__general_bonus(old_block, target_block, new_block)
		bonus += self.__point1(new_block, target_block) - self.__point1(old_block, target_block)

		#return point we got
		return bonus

	def catalyst_point(self, index):
		'''
		return the point of catalyst on selected tank
		'''
		#prepare
		x, y = self._Chemsynth__catalyst_range(self.dom, index)
		temp = ChemsynthPoint(self.get_dom(), self.get_tar())
		block_changed = y-x

		#allocating enough space
		old_block = [0]*block_changed
		target_block = [0]*block_changed
		new_block = [0]*block_changed

		#filling the block
		copy(old_block, self.dom, x, y)
		copy(target_block, self.tar, x, y)
		temp.catalyst(index)
		copy(new_block, temp.dom, x, y)

		#calculating point
		bonus = temp.__point_side(index, -1, temp) + temp.__point_side(index, 1, temp)
		bonus -= self.__point_side(index, -1, temp) + self.__point_side(index, 1, temp)
		bonus += self.__general_bonus(old_block, target_block, new_block)
		bonus += self.__point1(new_block, target_block) - self.__point1(old_block, target_block)

		#return point we got
		return bonus

	def stirrer_point(self, index):	
		'''
		return the point of stirrer on selected tank
		'''
		#prepare
		temp = ChemsynthPoint(self.get_dom(), self.get_tar())
		#out of range mitigation
		if (index == 0) or (index == len(self.dom)-1):
			return 0

		#filling the block 
		old_block = [self.dom[index-1], self.dom[index+1]]
		target_block = [self.tar[index-1], self.tar[index+1]]
		temp.stirrer(index)
		new_block = [temp.dom[index-1], temp.dom[index+1]]

		#calculating point
		bonus = 0
		if self.dom[index-1] == self.dom[index+1]:
			return bonus
		bonus = temp.__point_side(index-1, -1, temp) + temp.__point_side(index+1, 1, temp)
		bonus -= self.__point_side(index-1, -1, temp) + self.__point_side(index+1, 1, temp)
		bonus += self.__general_bonus(old_block, target_block, new_block)
		bonus += self.__point1(new_block, target_block) - self.__point1(old_block, target_block)

		#return point we got
		return bonus

	def centrifuge_point(self, index):
		'''
		return the point of centrifuge on selected tank
		'''
		#prepare
		max_range = self._Chemsynth__centrifuge_far(len(self.dom), index)
		temp = ChemsynthPoint(self.get_dom(), self.get_tar())		#value // 2 == value >> 1
		block_changed = max_range << 1					#value * 2 == value << 1

		#allocating enough space
		old_block = [0]*block_changed
		target_block = [0]*block_changed
		new_block = [0]*block_changed

		#filling the block
		self.__centrifuge_copy(old_block, self.dom, index, max_range)
		self.__centrifuge_copy(target_block, self.tar, index, max_range)
		temp.centrifuge(index)
		self.__centrifuge_copy(new_block, temp.dom, index, max_range)

		#calculating point
		bonus = -1 if (index == 1 or index == len(self.dom)-2) else 0	#block at 1 or len-1 is stirrer's job
		bonus += temp.__point_side(index-max_range, -1, temp) + temp.__point_side(index+max_range, 1, temp)
		bonus -= self.__point_side(index-max_range, -1, temp) + self.__point_side(index+max_range, 1, temp)
		bonus += self.__general_bonus(old_block, target_block, new_block)
		bonus += self.__point2(new_block, target_block) - self.__point2(old_block, target_block)

		#return point we got
		return bonus