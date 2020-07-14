#import standard library required
import argparse
import sys

#import tool required
from chemsynth import Chemsynth, ChemsynthException
from chempoint import ChemsynthPoint, ChemsynthPointException
from helper_func import find

#######################################################################################
########################################Execute########################################
#######################################################################################
def execute(chem, list1):
	'''
	executing chem with specified function's index and item's index
	'''
	#prepare
	#list of function
	#this is related to function best_route localvar func_point
	funcs = [Chemsynth.centrifuge, Chemsynth.stirrer, Chemsynth.catalyst, Chemsynth.replicator]

	#executing
	for f_idx, index in list1:
		funcs[f_idx](chem, index)

#######################################################################################
########################################Step 1#########################################
#######################################################################################
def bruteforce(chem, func):
	'''
	return list of point from func, related to best_route function
	'''
	#prepare
	temp = [0]*len(chem.dom)

	#get list of point from bruteforcing with func on each item
	for index in range(len(chem.dom)):
		temp[index] = func(chem, index)

	#return list of point
	return temp
		
def best_route(chem):
	'''
	get the best route from list of list of point from function in ChemsynthPoint
	'''
	#prepare
	#list of point function
	#this is related to function execute localvar funcs
	func_point = [ChemsynthPoint.centrifuge_point, ChemsynthPoint.stirrer_point, ChemsynthPoint.catalyst_point, ChemsynthPoint.replicator_point]

	#there are four function, each of them will be bruteforced to get list of point
	ways = [[],[],[],[]]
	max_value = 0
	max_index = 0
	func_index = 0

	#start to get list of point
	for i in (0,1,2,3):
		#get list of point from func_point[i]
		ways[i] = bruteforce(chem, func_point[i])

		#calculating the best route
		if max(ways[i]) > max_value:
			max_value = max(ways[i])
			max_index = find(ways[i],max(ways[i]))
			func_index = i

	#return function-index, index of item, and it's point
	return (func_index, max_index, max_value)

def step1(chem, change=False):
	'''
	step 1 responsible for returning to_do_list which is list of function's index and item's index
	'''
	#prepare
	step = 1
	to_do_list = []
	temp = chem
	if change == False:
		temp = ChemsynthPoint(chem.get_dom(), chem.get_tar())

	#while domain color != target color
	while temp.dom != temp.tar:
		#early break if 15 step has been produced
		if step == 16: break

		#getting function's index, item's index, and it's point
		f_idx, idx, point = best_route(temp)

		#point <= 0 means, bad if we continuing to do it, so just break
		if point <= 0:
			break

		#execute temp with specified function's index and item's index
		execute(temp, [[f_idx, idx]])

		#append to_do_list
		to_do_list.append((f_idx, idx))
		step += 1

	#return it
	return to_do_list

#######################################################################################
########################################Step 2#########################################
#######################################################################################
def get_not_finish(list1, list2):
	'''
	generating index of item that is not same with other item in the same index
	'''
	#prepare
	temp = []

	#search for index of different item same index and append to temp
	for i in range(len(list1)):
		if list1[i] != list2[i]:
			temp.append(i)

	#return list of index of different-item same-index
	return temp

def is_safe(list1, index, direction):
	'''
	checking safe condition
	safe conditions occur if the color at the index is not the same as the color on the left or right, based on
	direction. direction = -1 left, diretion = 1 right
	'''
	#item is safe if item is edge of list
	if direction == 1 and index == len(list1)-1:
		return True				#safe
	if direction == -1 and index == 0:
		return True				#safe

	#check if not safe
	if list1[index] == list1[index+direction]:
		return False			#not safe
	#else it's safe
	return True					#safe

def stirrer_index_help(list1, index, direction):
	'''
	generate the rightmost or leftmost based on direction i for stirrers which can later be used to help or 
	return -1 if it can't help. direction = -1 left, direction = 1 right
	'''
	#prepare
	y = 0 if direction == -1 else len(list1)-1

	#searching for index that can help later
	for i in range(index + 2*direction, y, 2*direction):
		if list1[i-1] != list1[i+1]:
			return i

	#fail
	return -1			#return -1 if fail

def centrifuge_index_help(list1, index, direction):
	'''
	generate i for centrifuges which can later be used to help or return a -1 if it can't help. direction = -1 
	left, direction = 1 right
	'''
	#prepare
	y = -1 if direction == -1 else len(list1)

	#searching for index that can help later
	for i in range(index + 2*direction, y, direction):
		max = Chemsynth._Chemsynth__centrifuge_far(len(list1), i)
		if index+direction == i-max*direction and list1[i-max] != list1[i+max]:
			return i

	#fail
	return -1			#return -1 if fail

def make_safe(list1, index, direction):
	'''
	generating list of [func, index] that make safe, if list empty means fail
	'''
	#prepare
	stirrer_index = stirrer_index_help(list1, index, direction)
	centrifuge_index = centrifuge_index_help(list1, index, direction)
	temp = []

	#0 = index for centifuge and 1 = index for stirrer, related to function execute localvar funcs

	#if stirrer only one step and not fail, do with stirrer
	if abs(index - stirrer_index) == 2 and stirrer_index != -1:
		temp.append([1, stirrer_index])

	#if stirrer step more than one, prefer centrifuge if able
	elif centrifuge_index != -1:
		temp.append([0, centrifuge_index])

	#if stirrer step more than one and centrifuge fail, do with stirrer
	elif stirrer_index != -1:
		for i in range(stirrer_index, index, 2*direction*-1):
			temp.append([1, i])

	#return [func, index]
	return temp

def go_and_back(chem, index):
	'''
	return go list and back list to make safe item that is not safe otherwise return empty, list means fail 
	'''
	#prepare
	left_list, right_list, left_list_back, right_list_back = [], [], [], []
	is_left_not_safe, is_right_not_safe = False, False

	#make left safe if left not safe
	if not(is_safe(chem.dom, index, -1)):
		left_list = make_safe(chem.dom, index, -1)
		is_left_not_safe = True

	#make right safe if right not safe
	if not(is_safe(chem.dom, index, 1)):
		right_list = make_safe(chem.dom, index, 1)
		is_right_not_safe = True

	#if not safe and fail to make safe
	if (is_left_not_safe and not(left_list)) or (is_right_not_safe and not(right_list)):
		return [[], [], 0] 					#0 is indicator if it fail to make safe

	#generating go and back list
	go = left_list + right_list
	left_list_back = list(left_list)
	right_list_back = list(right_list)
	left_list_back.reverse()
	right_list_back.reverse()
	back = left_list_back + right_list_back

	#return list of go and back
	return [go, back, 1]					#1 is indicator if it success to make safe or already safe

def step2(chem, change=False):
	'''
	generating step that will fix item that is not fixed if possible
	'''
	#prepare
	not_finished = get_not_finish(chem.dom, chem.tar)
	to_do_list = []
	temp = chem
	if change == False:
		temp = ChemsynthPoint(chem.get_dom(), chem.get_tar())

	#generating list of [func, index]
	for index in not_finished:
		while temp.dom[index] != temp.tar[index]:
			#getting go list, back list and it's state
			go, back, state = go_and_back(temp, index)

			#if fail to make safe, skip it
			if not(go) and not(back) and not(state):
				break

			#if fail to make safe because already safe
			if not(go) and not(back) and state:
				#do catalyst while safe state
				while temp.dom[index] != temp.tar[index] and is_safe(temp.dom, index, -1) and is_safe(temp.dom, index, 1):
					#2 = index for catalyst, related to function execute localvar funcs
					#catalyst it and append it
					temp.catalyst(index)
					to_do_list.append([2, index])
				#get out, already safe and hopefully fixed
				continue

			#executing go list
			execute(temp, go)

			#add go list to to_do_list
			to_do_list += go

			#do catalyst while safe state
			while temp.dom[index] != temp.tar[index] and is_safe(temp.dom, index, -1) and is_safe(temp.dom, index, 1):
				#2 = index for catalyst, related to function execute localvar funcs
				#catalyst it and append it
				temp.catalyst(index)
				to_do_list.append([2, index])

			#executing back list
			execute(temp, back)

			#add back list to to_do_list
			to_do_list += back

	#return to_do_list 
	return to_do_list

def prepare(to_do_list):
	'''
	this function will format to_do_list so it will be do_list. format means remove repeating same function
	on same index sequentially and append the count of it to the to do_list 
	'''
	#prepare
	f_idx, idx = to_do_list[0]
	x = 1
	do_list = []

	#formatting to_do_list
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

	#return do_list
	return do_list

def percentage(chem): 				#percentage of equality
	value = chem._ChemsynthPoint__point1(chem.dom, chem.tar)
	length = len(chem.dom)
	value = int((value / length) * 100)
	return value

def route(chem, do_list, advance=False):
	#list of tool name related to function execute localvar funcs
	func_name = ["\"Centrifuge\"", "\"Stirrer\"", "\"Catalyst\"", "\"Replicator\""]

	step = 1
	#table header
	print("{step:^5} {tool:^12} {block:^12} {times:^12} {complete:^12}".format(step='STEP', tool='TOOL', block='BLOCK', times='TIMES', complete='COMPLETE'))

	for f_idx, idx, x in do_list:
		#get old chemsynth tank
		temp = repr(chem)

		#executing as many as x
		for y in range(x):
			execute(chem, [[f_idx, idx]])

		#print the step
		
		#content
		print("{step:<5} {tool:^12} {block:^12} {times:^12} {complete:^12}".format(step='#'+str(step), tool=func_name[f_idx], block=idx+1, times=x, complete=str(percentage(chem))+'%'))

		#if advance argument specified print with tank state
		if advance == True:
			print(temp, "->", chem)

		step += 1

def get_parser():
	'''
	preparing for argument parser
	'''
	parser = argparse.ArgumentParser(prog='Chemsynth Router', description='Chemsynth Router by whoami and mrx', add_help=False)

	parser.add_argument('-a', '--advance', action='store_const', const=1, default=0, dest='advance', help='show step with realtime Chemsynth Tank color state')
	parser.add_argument('-d', '--doc', action='store_const', const=1, default=0, dest='doc', help='documentation about Chemsynth Router')
	parser.add_argument('-h', '--help', action='store_const', const=1, default=0, dest='help', help='show this help message')
	parser.add_argument('-q', '--quit', action='store_const', const=1, default=0, dest='quit', help='quit from program')
	parser.add_argument('-r', '--route', action="extend", nargs=2, help='route based on DOMAIN and TARGET, [COLOR] can be R, Y, G, B, P', metavar='[COLOR]', dest='route')
	parser.add_argument('-v', '--version', action='store_const', const=1, default=0, dest='version', help='show program version')

	return parser

def arg_check(Namespace):
	'''
	optional argument specified more than one in one line
	'''
	if Namespace.doc + Namespace.version + Namespace.quit + Namespace.help + int(bool(Namespace.route)) > 1:
		raise ArgumentError
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
              "source available at https://github.com/0xwhoami/Growtopia-Chemsynth-Router-V2\n")

def help(parser):
	parser.print_help()

def quit():
	raise SystemExit2

def version():
	print("Chemsynth Router 2.0")

#######################################################################################
#########################################error#########################################
#######################################################################################
class SystemExit2(Exception): pass
class ArgumentError(Exception): pass 

#######################################################################################
#########################################start#########################################
#######################################################################################

welcome()

#get parser for argument
parser = get_parser()

while True:
	try:
		to_do_list = []
		result = parser.parse_args(input(">>> ").split())

		#checking argument
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
			#get domain and target
			dom = result.route[0]
			tar = result.route[1]

			#prepare
			chem = ChemsynthPoint(dom, tar)
			temp = ChemsynthPoint(dom, tar)

			#routing
			to_do_list = step1(temp, True)
			to_do_list += step2(temp, True)

			#we can't route
			if to_do_list == []:
				print("sorry we can't route, it's the maximum we can do :(")
				continue

			do_list = prepare(to_do_list)

			#print route step by step
			route(chem, do_list, result.advance)

	except (ChemsynthException, ChemsynthPointException) as e:
		print("error:", e)
	except (ArgumentError, EOFError, KeyboardInterrupt):
		help(parser)
	except SystemExit2:
		sys.exit(0)
	except SystemExit:
		pass
	except:
		#logging
		log = open('log.txt', 'a')
		print("error:", sys.exc_info()[:2], '\n',
			  "arg:", result,
			  file=log, end='\n\n')
		log.close()
		raise