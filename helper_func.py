def find(list1, item):
	'''
	look for the first and the same item, return index
	'''
	i = 0
	for x in list1:
		if x == item:
			return i
		i += 1
	return i

def range_max(list1,index):
	'''
	look for the numbers that are most likely to be added to the index so they are not out of range
	'''
	x = 1 if len(list1)%2 else 0 
	a = 0
	if (index == 0) or (index == len(list1)-1):
		return a
	for x in range(1,len(list1)//2+x):
		if (index+x != len(list1)) and (index-x != -1):
			a += 1
		else:
			break
	return a

def color_changer(tank,index):
	'''
	this function changed the item color to the next
	'''
	color_list = ('R','Y','G','B','P')
	a = find(color_list, tank[index])
	tank[index] = color_list[(a+1)%5]

def copy(list1, list2, index=0, n=0, step=1): #copying from list2 to list1 start at index till n item
	x = 0
	for i in range(index, n, step):
		list1[x] = list2[i]
		x += 1
