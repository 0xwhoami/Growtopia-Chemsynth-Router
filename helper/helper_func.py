__all__ = ['find',
           'copy']

def find(list1, item):
	'''
	look for the first and the same item, return index if found
	if i == len(list1) then raise NotFound
	'''
	for index in range(len(list1)):
		if list1[index] == item:
			return index

	raise ValueError("%s not found" % (item))

def copy(list1, list2, index=0, n=0, step=1):
	'''
	copying from list2 to list1 start at index till n item
	'''
	x = 0
	for i in range(index, n, step):
		list1[x] = list2[i]
		x += 1
