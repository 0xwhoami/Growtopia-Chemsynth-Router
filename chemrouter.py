#!/usr/bin/env python

"""
Copyright (c) 2020-End_Of_Life
See the file 'LICENSE' for copying permission
"""

# import standard library required
import argparse
import sys

# import tool required
from route.route import route
from route.execute import execute
from chemsynth.chemsynth import Chemsynth, ChemsynthException
from chemsynth.chempoint import ChemsynthPoint, ChemsynthPointException

# =========
# Interface
# =========

def prepare(to_do_list):
	'''
	this function will format to_do_list so it will be do_list. format means remove repeating same function
	on same index sequentially and append the count of it to the to do_list 
	'''
	# prepare
	f_idx, idx = to_do_list[0]
	x = 1
	do_list = []

	# formatting to_do_list
	for i in range(1, len(to_do_list)):
		f_idx2, idx2 = to_do_list[i]
		if f_idx == f_idx2 and idx == idx2:
			x += 1
			continue
		do_list.append([f_idx, idx, x])
		f_idx = f_idx2
		idx = idx2
		x = 1
	do_list.append([f_idx, idx, x])

	# return do_list
	return do_list

def percentage(dom, tar):
	'''
	return percentage of equality
	'''
	value = ChemsynthPoint._ChemsynthPoint__point1(dom, tar)
	length = len(dom)
	value = int((value / length) * 100)
	return value

def print_step(dom, tar, do_list, advance=False):
	# list of tool name sorted based on index of function in execute.py
	func_name = ["\"Centrifuge\"", "\"Stirrer\"", "\"Catalyst\"", "\"Replicator\""]

	# prepare
	chem = Chemsynth(dom)
	tar = tar.upper()
	step = 1

	# table header
	print("{step:^5} {tool:^12} {block:^12} {times:^12} {complete:^12}".format(step='STEP', tool='TOOL', block='BLOCK', times='TIMES', complete='COMPLETE'))

	for f_idx, idx, x in do_list:
		# get old chemsynth tank
		temp = str(chem)

		# executing as many as x
		for y in range(x):
			execute(chem, [[f_idx, idx]])

		# print the step and the content
		print("{step:<5} {tool:^12} {block:^12} {times:^12} {complete:^12}".format(step='#'+str(step), tool=func_name[f_idx], block=idx+1, times=x, complete=str(percentage(chem.dom, tar))+'%'))

		# if advance == True, print with tank state
		if advance == True:
			print(temp, "->", chem)

		step += 1

def get_parser():
	'''
	preparing for argument parser
	'''
	parser = argparse.ArgumentParser(prog='Chemsynth Router', description='Chemsynth Router by whoami and mrx', add_help=False)
	group = parser.add_mutually_exclusive_group()

	group.add_argument('-d', '--doc', action='store_const', const=1, default=0, dest='doc', help='documentation about Chemsynth Router')
	group.add_argument('-h', '--help', action='store_const', const=1, default=0, dest='help', help='show this help message')
	group.add_argument('-q', '--quit', action='store_const', const=1, default=0, dest='quit', help='quit from program')
	group.add_argument('-r', '--route', action="extend", nargs=2, help='route based on DOMAIN and TARGET, [COLOR] can be R, Y, G, B, P', metavar='[COLOR]', dest='route')
	parser.add_argument('-a', '--advance', action='store_const', const=1, default=0, dest='advance', help='show step with realtime Chemsynth Tank color state, optionally with -r/--route')
	group.add_argument('-v', '--version', action='store_const', const=1, default=0, dest='version', help='show program version')

	return parser

def arg_check(Namespace):
	'''
	optional argument specified more than one in one line
	'''
	if Namespace.doc + Namespace.version + Namespace.quit + Namespace.help + Namespace.advance > 1:
		raise ArgumentError
	if Namespace.advance == 1 and not(any([Namespace.doc, Namespace.version, Namespace.quit, Namespace.help, Namespace.route])):
		raise ArgumentError

def welcome():
	print("Chemsynth Router [Version 2.0] by whoami and mrx\n"
	      "type -h or --help for more informations\n")

def doc():
	print("Chemsynth Router v 2.0 is an open source program written in Python 3\n"
	      "created by whoami and mrx\n"
	      "source available at https://github.com/0xwhoami/Growtopia-Chemsynth-Router\n")

def help(parser):
	parser.print_help()

def quit():
	raise SystemExit2

def version():
	print("Chemsynth Router 2.0")

# =====
# Error
# =====

class SystemExit2(Exception): pass
class ArgumentError(Exception): pass 

# =====
# Start
# =====

welcome()

# get parser for argument
parser = get_parser()

while True:
	try:
		to_do_list = []
		result = parser.parse_args(input(">>> ").split())

		# checking argument
		arg_check(result)

		if result.doc:
			doc()

		elif result.help:
			help(parser)

		elif result.quit:
			quit()

		elif result.version:
			version()

		elif result.route:
			# get domain and target
			dom = result.route[0]
			tar = result.route[1]

			# routing
			to_do_list = route(dom, tar)

			# we can't route
			if to_do_list == []:
				print("sorry we can't route, it's the maximum we can do :(")
				continue

			do_list = prepare(to_do_list)

			# print route step by step
			print_step(dom, tar, do_list, result.advance)

	except (ChemsynthException, ChemsynthPointException) as e:
		print("error:", e)
	except (ArgumentError, EOFError, KeyboardInterrupt):
		help(parser)
	except SystemExit2:
		sys.exit(0)
	except SystemExit:
		pass
	except:
		# logging
		log = open('log.txt', 'a')
		print("error:", sys.exc_info()[:2], '\n',
		      "arg:", result,
		      file=log, end='\n\n')
		log.close()
		raise
