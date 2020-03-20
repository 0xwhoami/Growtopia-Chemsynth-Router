from chemsynth_point import *

func_point = [Chemsynth_point.centrifuge_point, Chemsynth_point.stirrer_point, Chemsynth_point.catalyst_point, Chemsynth_point.replicator_point]
funcs = [Chemsynth.centrifuge, Chemsynth.stirrer, Chemsynth.catalyst, Chemsynth.replicator]
func_name = ["\"Centrifuge\"", "\"Stirrer\"", "\"Catalyst\"", "\"Replicator\""]

def __point(list1, list2): 			#point
	value = 0
	length = len(list1)
	for i in range(len(list1)):
        	if list1[i] == list2[i]:
        		value += 1
	value = (10 // length) *10
	return value

def bruteforce(chem, func):			#return list of point from function
	tmp = [0]*len(chem.dom)
	for index in range(len(chem.dom)):
		tmp[index] = func(chem, index)
	return tmp
		
def best_route(chem):			#get the best route from list of list of point from function
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
		
def do(chem, f_idx, idx, step):			#execute function on domain
	print("#%-3d from %s %s to block number %d -> " %(step, chem.dom, func_name[f_idx], idx+1), end = '')
	funcs[f_idx](chem, idx)
	print(chem.dom, "complete = %d%%"%(__point(chem.dom, chem.tar)))

def step1(chem, step = 1):			#basic step
	printed = False
	while chem.dom != chem.tar:
		f_idx, idx, point = best_route(chem)
		if point <= 0:
			break
		do(chem, f_idx, idx, step)
		step += 1

print("R = Red, Y = Yellow, G = Green, B = Blue, and P = Pink")
print("10 Blocks of current tank, and 10 Blocks for target tank\n")

dom = input("Type the colors of your current Chemsynth Tank: ").upper()
tar = input("Type the colors of your target Chemsynth Tank: ").upper()

chem = Chemsynth_point(list(dom), list(tar))
step1(chem)

input("Press enter to quit")
