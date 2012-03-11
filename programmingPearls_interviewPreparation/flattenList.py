
def flattenByOne(E):
	n = len(E)
	if n==0:
		return E
	if n==1:
		return E[0]
	else:
		return reduce(lambda acc,L: acc+L, E, [])

E = [[1,2,32], [2,2,[23,24]], [4,[[23],2],6,[7],3]]

flattenByOne(E)






def flattenAll(E):
	if type(E) is list:
		n = len(E)
		if n==0:
			return []
		if n==1:
			return flattenAll(E[0])
		else:
			return reduce(lambda acc,L: acc+flattenAll(L), E, [])
	else:
		return [E]
		

flattenAll(E)