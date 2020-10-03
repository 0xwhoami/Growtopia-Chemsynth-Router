#!/usr/bin/env python

"""
Copyright (c) 2020-End_Of_Life
See the file 'LICENSE' for copying permission
"""

# absolute import
from random import randint
from helper.helper_func import find

__all__ = ['Chemsynth',
           'ChemsynthException'
          ]

# ======
# Colors
# ======

RED = 0
YELLOW = 1
GREEN = 2
BLUE = 3
PINK = 4

# ===================
# Chemsynth Exception
# ===================

class ChemsynthException(Exception): pass
class UnspecifiedColor(ChemsynthException): pass
class UnidentifiedColor(ChemsynthException): pass

# =============================
# Utility functions and classes
# =============================

class Chemsynth:
	'''
	"Tired of the lousy chemicals nature has to offer? Create new synthetic ones! With a Rare
	Chemsynth Processor, Chemsynth Tanks, and one each of the five Chemsynth tools, you
	can be whipping up Synthetic Chemicals in no time. Warning: Chemsynth solving is a pretty
	tricky puzzle, and it costs a whole bunch of the five basic chemicals (R, G, B, P, and Y) to
	complete."
	'''

	# ============
	# Class Member
	# ============

	__slots__ = ['_dom']
	_virtual = ['dom']

	# list of expected input color string
	color_table = ('R', 'Y', 'G', 'B', 'P')

	# ========================
	# Class Building Functions
	# ========================

	def __init__(self, dom):
		# validating input color
		self.__color_validation(dom)

		# initialization
		self._dom = list(dom.upper().strip()) 

		# encode color
		self._encode_color(self._dom)

	def __repr__(self):
		return repr(self._dom)

	def __str__(self):
		temp = self._dom.copy()
		self._decode_color(temp)

		return "[" + "|".join(temp) + "]"

	def __getattr__(self, name):
		'''
		fetching a virtual attribute, virtual attribute is used
		when fecthing an attribute in _virtual to make a new
		instance
		'''
		if name in self._virtual:
			temp = object.__getattribute__(self, '_' + name).copy()
			self._decode_color(temp)
			return ''.join(temp)

		raise AttributeError("%s object has no attribute %s" %(self.__class__.__name__, name))

	@staticmethod
	def _encode_color(dom):
		'''
		encode color to index based on Chemsynth.color_table
		'R' -> RED
		'Y' -> YELLOW
		'G' -> GREEN
		'B' -> BLUE
		'P' -> PINK
		'''
		for index in range(len(dom)):
			dom[index] = find(Chemsynth.color_table, dom[index])

	@staticmethod
	def _decode_color(dom):
		'''
		decode index to color based on Chemsynth.color_table
		RED    -> 'R'
		YELLOW -> 'Y'
		GREEN  -> 'G'
		BLUE   -> 'B'
		PINK   -> 'P'
		'''
		for index in range(len(dom)):
			dom[index] = Chemsynth.color_table[dom[index]]

	# ================
	# Interface Helper
	# ================

	@staticmethod
	def __color_validation(color_string):
		'''
		validating input color based on Chemsynth.color_table
		'''
		# prepare
		temp = color_string.upper().strip()

		# test for empty color
		if temp == "":
			raise UnspecifiedColor("color not specified")

		# test for unidentified color
		for index in range(len(temp)):
			if not(temp[index] in Chemsynth.color_table):
				raise UnidentifiedColor("unidentified color: '%s'" % (color_string[index]))

	@staticmethod
	def __centrifuge_far(length, index):
		'''
		produce a maximum block distance that can be affected by a centrifuge
		'''
		mid = length >> 1						# length // 2
		max_value = (mid) - ((length & 1)^1)	# length % 2 == length & 1

		# calculating
		# upper than mid
		if index > mid:
			return max_value - index + mid

		# mid
		elif index == mid:
			return max_value

		# lower than mid
		return index

	@staticmethod
	def __catalyst_range(tank, index):
		'''
		produce a maximum block range that can be affected by a catalyst
		'''
		start, end = index, index

		# calculating start index
		while start-1 > -1 and tank[start-1] == tank[index]:
			start -= 1

		# calculating end index
		while end+1 < len(tank) and tank[end+1] == tank[index]:
			end += 1

		return (start, end+1)

	# =========
	# Interface
	# =========

	def solvent(self, index):
		'''
		Use on a highlighted Chemsynth Tank to dissolve it,
		shifting chemicals left to fill in the gap. A random
		chemical is added in the rightmost tank.
		'''
		# shifting block to the left
		for i in range(1, len(self._dom)):
			self._dom[i-1] = self._dom[i]

		# random color in rightmost tank
		self._dom[len(self._dom)-1] = randint(0, len(self._dom)-1)

	def replicator(self, index):
		'''
		Use on a highlighted Chemsynth Tank to duplicate its
		content, pushing all chemicals to the right to make
		room.
		'''
		# shifting block to the right start at index till len-1 but doing from right
		for i in range(len(self._dom)-1, index, -1):
			self._dom[i] = self._dom[i-1]

	def catalyst(self, index):
		'''
		Use on a highlighted Chemsynth Tank to shift its color
		upward on the spectrum (Red, Yellow, Green, Blue,
		Pink, Red). This also affects all touching tanks of the
		same color.
		'''
		# get range start from x, end at y (excluding y)
		start, after_end = self.__catalyst_range(self._dom, index)

		# change color to the next color
		self._dom[index] = (self._dom[index] + 1) % len(Chemsynth.color_table)

		# side effect of catalyst, affect all the same color before color changed
		for i in range(start, after_end):
			self._dom[i] = self._dom[index]

	def stirrer(self, index):
		'''
		Use on a highlighted Chemsynth Tank to swap the
		chemicals on either side of it with each other. The
		selected tank is unaffected.
		'''
		# out of range mitigation
		if not(index == 0 or index == len(self._dom)-1):
			# swap color
			self._dom[index-1], self._dom[index+1] = self._dom[index+1], self._dom[index-1]

	def centrifuge(self, index):
		'''
		Use on a highlighted Chemsynth Tank to rotate 
		chemicals around it. Rotates as many from the right
		as it can to match how many are to the left of the
		selected tank.
		'''
		# get the maximum distance that can be reached by centrifuge
		range_plus_or_minus = self.__centrifuge_far(len(self._dom), index)

		# swap color
		for x in range(1, range_plus_or_minus+1):
			self._dom[index-x], self._dom[index+x] = self._dom[index+x], self._dom[index-x]
