from os import system
from chemsynth import *
from chempoint import *
from helper_func import find

'''
func_point = [ChemsynthPoint.centrifuge_point, ChemsynthPoint.stirrer_point, ChemsynthPoint.catalyst_point, ChemsynthPoint.replicator_point]
funcs = [Chemsynth.centrifuge, Chemsynth.stirrer, Chemsynth.catalyst, Chemsynth.replicator]
func_name = ["\"Centrifuge\"", "\"Stirrer\"", "\"Catalyst\"", "\"Replicator\""]
'''

def __percentage(chem): 				#percentage of equality
	value = chem._ChemsynthPoint__point1(chem.dom, chem.tar)
	length = len(chem.dom)
	value = int((value / length) * 100)
	return value

def argChk(list1):						#validating argument
	for item in list1:
		if not(item in Chemsynth.color_table):
			return False
	return True

def bruteforce(chem, func):					#return list of point from function
	tmp = [0]*len(chem.dom)
	for index in range(len(chem.dom)):
		tmp[index] = func(chem, index)
	return tmp
		
def best_route(chem):						#get the best route from list of list of point from function
	func_point = [ChemsynthPoint.centrifuge_point, ChemsynthPoint.stirrer_point, ChemsynthPoint.catalyst_point, ChemsynthPoint.replicator_point]
	ways = [[],[],[],[]]
	max_value = 0
	max_index = 0
	func_index = 0
	for i in (0,1,2,3):
		ways[i] = bruteforce(chem, func_point[i])
		if max(ways[i]) > max_value:
			max_value = max(ways[i])
			max_index = find(ways[i],max(ways[i]))
			
			func_index = i

	return (func_index, max_index, max_value)
		
def do(chem, f_idx, idx):					#execute function on domain
	funcs = [Chemsynth.centrifuge, Chemsynth.stirrer, Chemsynth.catalyst, Chemsynth.replicator]
	funcs[f_idx](chem, idx)

def step1(chem):						#basic step
	step = 1						#return to do list for best route
	to_do_list = []
	while chem.dom != chem.tar:
		if step == 16: break				#early break if 15 step has been produced
		f_idx, idx, point = best_route(chem)
		if point <= 0:
			break
		do(chem, f_idx, idx)
		to_do_list.append((f_idx, idx))
		step += 1

	return to_do_list

def get_not_finish(list1, list2):			#generating index of unfinished blocks
	temp = []
	for i in range(len(list1)):
		if list1[i] != list2[i]:
			temp.append(i)
	return temp

def is_safe(list1, index, direction):
	'''
	safe conditions occur if the color at the index is not the same as the color on the left or right, based on
	direction. direction = -1 left, diretion = 1 right
	'''
	if direction == 1 and index == len(list1)-1:
		return True				#safe
	if direction == -1 and index == 0:
		return True				#safe
	if list1[index] == list1[index+direction]:
		return False				#not safe
	return True					#safe

def stirrer_index_help(list1, index, direction):
	'''
	generate the rightmost or leftmost based on direction i for stirrers which can later be used to help or 
	return a -1 if it can't help. direction = -1 left, direction = 1 right
	'''
	y = 0 if direction == -1 else len(list1)-1

	for i in range(index + 2*direction, y, 2*direction):
		if list1[i-1] != list1[i+1]:
			return i
	return -1			#return -1 if fail

def centrifuge_index_help(list1, index, direction):
	'''
	generate i for centrifuges which can later be used to help or return a -1 if it can't help. direction = -1 
	left, direction = 1 right
	'''
	y = -1 if direction == -1 else len(list1)
	for i in range(index + 2*direction, y, direction):
		max = Chemsynth._Chemsynth__centrifuge_far(len(list1), i)
		if index+direction == i-max*direction and list1[i-max] != list1[i+max]:
			return i
	return -1			#return -1 if fail

def make_safe(list1, index, direction):
	'''
	generating list of [func, index] that make safe, if list empty means fail
	'''
	stirrer_index = stirrer_index_help(list1, index, direction)
	centrifuge_index = centrifuge_index_help(list1, index, direction)
	temp = []
	if abs(index - stirrer_index) == 2 and stirrer_index != -1:		#stirrer only one step and not fail
		temp.append([1, stirrer_index])					#1 = index for stirrer
	elif centrifuge_index != -1:						#not fail
		temp.append([0, centrifuge_index])				#0 = index for centifuge
	elif stirrer_index != -1:						#not fail
		for i in range(stirrer_index, index, 2*direction*-1):
			temp.append([1, i])					#1 = index for stirrer
	return temp

def go_and_back(chem, index):
	'''
	return go list and back list to make safe item that is not safe otherwise return empty list means fail 
	'''
	left_list, right_list, left_list_back, right_list_back = [], [], [], []
	is_left_not_safe, is_right_not_safe = False, False

	if not(is_safe(chem.dom, index, -1)):
		left_list = make_safe(chem.dom, index, -1)
		is_left_not_safe = True

	if not(is_safe(chem.dom, index, 1)):
		right_list = make_safe(chem.dom, index, 1)
		is_right_not_safe = True

	if (is_left_not_safe and not(left_list)) or (is_right_not_safe and not(right_list)):	#if not safe and fail to make safe
		return [[], [], 0] 					#fail

	go = left_list + right_list
	left_list_back = list(left_list)
	right_list_back = list(right_list)
	left_list_back.reverse()
	right_list_back.reverse()
	back = left_list_back + right_list_back

	return [go, back, 1]						#success or already safe

def step2(chem):
	'''
	generating step that will fix item that is not fixed if possible
	'''
	not_finished = get_not_finish(chem.dom, chem.tar)
	temp = []
	for index in not_finished:
		while chem.dom[index] != chem.tar[index]:
			go, back, state = go_and_back(chem, index)
			if not(go) and not(back) and not(state):			#fail to make safe
				break							#skip it
			if not(go) and not(back) and state:				#already safe
				while chem.dom[index] != chem.tar[index] and is_safe(chem.dom, index, -1) and is_safe(chem.dom, index, 1):
					chem.catalyst(index)
					temp.append([2, index])				#catalyst code
				continue
			execute2(chem, go)
			temp += go
			while chem.dom[index] != chem.tar[index] and is_safe(chem.dom, index, -1) and is_safe(chem.dom, index, 1):
				chem.catalyst(index)
				temp.append([2, index])					#catalyst code
			execute2(chem, back)
			temp += back
	return temp

def prepare(to_do_list):					#this function will format to_do_list
	f_idx, idx = to_do_list[0]
	x = 1
	do_list = []
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
	return do_list

def execute(chem, do_list):				#this funtion printing do_list out step by step
	func_name = ["\"Centrifuge\"", "\"Stirrer\"", "\"Catalyst\"", "\"Replicator\""]
	step = 1
	for f_idx, idx, x in do_list:
		print("#%-2d %s %-12s on block %-2d %dx -> " %(step, chem, func_name[f_idx], idx+1, x), end = '')
		for y in range(x):
			do(chem, f_idx, idx)
		print(chem, "complete = %d%%" % (__percentage(chem)))
		step += 1

def execute2(chem, list1):
	for f_idx, index in list1:
		do(chem, f_idx, index)

def en(string):
	temp = ''
	for char in string:
		temp += chr(ord(char)^1)
	return temp

#The Start of the program

print(en('Bidlrxoui!Sntuds!ZWdsrhno!3\\!cx!vin`lh!`oe!lsy\x0bS!<!Sde-!X!<!Xdmmnv-!F!<!Fsddo-!C!<!Cmtd-!`oe!Q!<!Qhoj\x0b01!Cmnbjr!ng!btssdou!u`oj-!`oe!01!Cmnbjr!gns!u`sfdu!u`oj\x0b'))

while True:
	to_do_list = []
	dom = input("Type colors of domain Chemsynth Tank: ").upper().strip()
	tar = input("Type colors of target Chemsynth Tank: ").upper().strip()
	if not(dom) and not(tar):
		system("cls")			#clear screen
		continue
	if len(dom) == len(tar) and argChk(dom) and argChk(tar):
		chem = ChemsynthPoint(dom, tar)
		chem2 = ChemsynthPoint(dom, tar)
		to_do_list = step1(chem)
		for x in range(len(chem.dom) // 2):
			to_do_list += step2(chem)
		do_list = prepare(to_do_list)
		execute(chem2, do_list)
		print('='*96)					#break line
		continue
	print("invalid argument, please type correctly!")