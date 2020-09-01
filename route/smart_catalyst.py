# absolute import
from chemsynth.chemsynth import Chemsynth
from chemsynth.chempoint import ChemsynthPoint

# relative import
from .execute import execute
from .execute import CENTRIFUGE, STIRRER, CATALYST, REPLICATOR

__all__ = ['smart_catalyst']

# direction
LEFT = -1
RIGHT = 1

# condition
SUCCESS = 1
FAIL = -1

def _get_not_finish(list1, list2):
	'''
	return list of index of item that is differ with other item at the same index
	'''
	# prepare
	temp = []

	# search for index of different item same index and append to temp
	for index in range(len(list1)):
		if list1[index] != list2[index]:
			temp.append(index)

	# return list of index of different-item same-index
	return temp

def _is_safe(list1, index, direction):
	'''
	checking safe condition, safe conditions occur if the color at the index is not the same as the
	color on the left or right, based on direction
	'''
	# item is safe if item is edge of list
	if (direction == LEFT and index == 0) or (direction == RIGHT and index == len(list1)-1):
		return True				# safe

	# check if not safe
	if list1[index] == list1[index+direction]:
		return False				# not safe
	# else it's safe
	return True					# safe

def _stirrer_index_help(list1, index, direction):
	'''
	generate the most possible stirrers index which can later be used to help or return FAIL
	'''
	# prepare
	y = 0 if direction == LEFT else len(list1)-1

	# searching for index that can help
	for i in range(index + 2*direction, y, 2*direction):
		if list1[i-1] != list1[i+1]:
			return i

	# fail
	return FAIL

def _centrifuge_index_help(list1, index, direction):
	'''
	generate the most possible centrifuges index which can later be used to help or return FAIL
	'''
	# prepare
	y = -1 if direction == LEFT else len(list1)

	# searching for index that can help
	for i in range(index + 2*direction, y, direction):
		max = Chemsynth._Chemsynth__centrifuge_far(len(list1), i)
		if index+direction == i-max*direction and list1[i-max] != list1[i+max]:
			return i

	# fail
	return FAIL

def _make_safe(list1, index, direction):
	'''
	return list of [func, index] that make safe, if list empty means fail
	'''
	# prepare
	stirrer_index = _stirrer_index_help(list1, index, direction)
	centrifuge_index = _centrifuge_index_help(list1, index, direction)
	temp = []

	# if stirrer only one step and not fail, do with stirrer
	if abs(index - stirrer_index) == 2 and stirrer_index != FAIL:
		temp.append([STIRRER, stirrer_index])

	# if stirrer step more than one, prefer centrifuge if able
	elif centrifuge_index != FAIL:
		temp.append([CENTRIFUGE, centrifuge_index])

	# if stirrer step more than one and centrifuge fail, do with stirrer
	elif stirrer_index != FAIL:
		for i in range(stirrer_index, index, 2*direction*-1):
			temp.append([STIRRER, i])

	# return [func, index] or empty list
	return temp

def _go_and_back(chem, index):
	'''
	return go list and back list to make safe item that is not safe, if list empty means fail
	'''
	# prepare
	left_list, right_list, left_list_back, right_list_back = [], [], [], []
	is_left_not_safe, is_right_not_safe = False, False

	# make left safe if left not safe
	if not(_is_safe(chem._dom, index, LEFT)):
		left_list = _make_safe(chem._dom, index, LEFT)
		is_left_not_safe = True

	# make right safe if right not safe
	if not(_is_safe(chem._dom, index, RIGHT)):
		right_list = _make_safe(chem._dom, index, RIGHT)
		is_right_not_safe = True

	# if not safe and fail to make safe
	if (is_left_not_safe and left_list == []) or (is_right_not_safe and right_list == []):
		return [[], [], FAIL]

	# generating go and back list
	go = left_list + right_list
	left_list_back = left_list.copy()
	right_list_back = right_list.copy()
	left_list_back.reverse()
	right_list_back.reverse()
	back = left_list_back + right_list_back

	# return list of go and back
	return [go, back, SUCCESS]

def smart_catalyst(chem):
	'''
	generating step that will fix item that is not fixed if possible.
	WARNING chem modified
	'''
	# prepare
	not_finished = _get_not_finish(chem._dom, chem._tar)
	to_do_list = []

	# generating list of [func, index]
	for index in not_finished:
		while chem._dom[index] != chem._tar[index]:
			# getting go list, back list and it's state
			go, back, state = _go_and_back(chem, index)

			# if fail to make safe, skip it
			if state == FAIL:
				break

			# if already safe, or success to make safe, let's do it
			else:
				# executing go list
				execute(chem, go)

				# add go list to to_do_list
				to_do_list += go

				# do catalyst while safe state
				while (chem._dom[index] != chem._tar[index] and _is_safe(chem._dom, index, LEFT) and
				       _is_safe(chem._dom, index, RIGHT)):
					# catalyst it and append it
					chem.catalyst(index)
					to_do_list.append([CATALYST, index])

				# executing back list
				execute(chem, back)

				# add back list to to_do_list
				to_do_list += back

	# return to_do_list
	return to_do_list
