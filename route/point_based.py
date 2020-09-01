#!/usr/bin/env python

"""
Copyright (c) 2020-End_Of_Life
See the file 'LICENSE' for copying permission
"""

# absolute import
from chemsynth.chempoint import ChemsynthPoint
from helper.helper_func import find

# relative import
from .execute import execute
from .execute import CENTRIFUGE, STIRRER, CATALYST, REPLICATOR

__all__ = ['point_route']

# ascending order based on value CENTRIFUGE, STIRRER, CATALYST, REPLICATOR
_func_point = (ChemsynthPoint.centrifuge_point, ChemsynthPoint.stirrer_point, ChemsynthPoint.catalyst_point,
              ChemsynthPoint.replicator_point)

def _bruteforce(chem, func):
	'''
	return list of point from func
	'''
	# prepare
	temp = [0]*len(chem._dom)

	# get list of point from bruteforcing with func on each item
	for index in range(len(chem._dom)):
		temp[index] = func(chem, index)

	# return list of point
	return temp
		
def _best_route(chem):
	'''
	get the best route from list of list of point from function in ChemsynthPoint
	'''
	# there are four function, each of them will be bruteforced to get list of point
	ways = [[],[],[],[]]
	max_value = 0
	max_index = 0
	func_index = 0

	# start to get list of point
	for i in (CENTRIFUGE, STIRRER, CATALYST, REPLICATOR):
		# get list of point from _func_point[i]
		ways[i] = _bruteforce(chem, _func_point[i])

		# calculating the best route
		if max(ways[i]) > max_value:
			max_value = max(ways[i])
			max_index = find(ways[i],max(ways[i]))
			func_index = i

	# return function-index, index of item, and it's point
	return (func_index, max_index, max_value)

def point_route(chem):
	'''
	return to_do_list which is list of function's index and item's index.
	WARNING chem modified
	'''
	# prepare
	to_do_list = []

	# while domain color != target color
	while chem._dom != chem._tar:
		# getting function's index, item's index, and it's point
		func_index, index, point = _best_route(chem)

		# point <= 0 means, bad if we continuing to do it, so just break
		if point <= 0:
			break

		# execute chem with specified function's index and item's index
		execute(chem, [[func_index, index]])

		# append step to to_do_list
		to_do_list.append((func_index, index))

	# return to_do_list
	return to_do_list
