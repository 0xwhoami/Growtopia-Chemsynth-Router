#!/usr/bin/env python

"""
Copyright (c) 2020-End_Of_Life
See the file 'LICENSE' for copying permission
"""

# absolute import
from chemsynth.chemsynth import Chemsynth

__all__ = ['execute']

# list of function, sorted based on priority
funcs = (Chemsynth.centrifuge, Chemsynth.stirrer, Chemsynth.catalyst, Chemsynth.replicator)

# index of function based on "funcs"
CENTRIFUGE = 0
STIRRER = 1
CATALYST = 2
REPLICATOR = 3
# SOLVENT = 4	# undefined

def execute(chem, do_list):
	'''
	executing chem with specified function's index and item's index
	'''
	#executing
	for f_idx, index in do_list:
		funcs[f_idx](chem, index)
