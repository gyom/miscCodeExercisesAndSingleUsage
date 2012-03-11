

class Node():
	# value
	# children : a list
	def __init__(self, value, children=[]):
		self.value = value
		self.children = children

class BinomialTree():
	# root of type Node
	# weight of type integer
	def __init__(self, BT1=None, BT2=None):
		if BT1 and BT2:
			(w1,w2) = (BT1.weight, BT2.weight)
			assert (w1==w2)
			self.weight = w1+w2
			(m1, m2) = (BT1.getMin(), BT2.getMin())
			if m1 > m2:
				self.root = Node(m2, BT2.root.children + [BT1])
			else:
				self.root = Node(m1, BT1.root.children + [BT2])
		elif BT1:
			# we'll assume here that BT1 is a Node and not a BinomialTree
			self.root = BT1
			self.weight = 1 + (len(BT1.children) if BT1.children else 0)
		elif BT2:
			# we'll assume here that BT2 is a Node and not a BinomialTree
			self.root = BT2
			self.weight = 1 + (len(BT2.children) if BT2.children else 0)
	def getMin(self):
		return self.root.value
	def toString(self):
		start = "[" + str(self.root.value) + " : "
		middle = reduce(lambda acc,e: acc + " " + e.toString(), self.root.children, "")
		end = "]"
		return start + middle + end


a1 = Node(3)
a2 = Node(5)
b1 = BinomialTree(a1)
b2 = BinomialTree(a2)
a3 = Node(2)
a4 = Node(19)
b3 = BinomialTree(a3)
b4 = BinomialTree(a4)

e = BinomialTree(BinomialTree(b1,b2), BinomialTree(b3,b4))
print e.toString()


def packByTwo(L):
	R = []
	left = [] if len(L)%2==0 else [L[-1]]
	i=0
	while(i+1 < len(L)):
		R.append( (L[i], L[i+1]) )
		i += 2
	return (R, left)

assert(packByTwo([]) == ([], []))
assert(packByTwo([1]) == ([], [1]))
assert(packByTwo([1,2,3]) == ( [(1,2)], [3] ) )
assert(packByTwo([1,2,3,4]) == ( [(1,2), (3,4)], [] ) )
assert(packByTwo([1,2,3,4,5]) == ( [(1,2), (3,4)], [5] ) )



class BinomialHeap():
	def __init__(self, *BTS):
		#self.table = {}
		self.table = dict( (pow(2,p), []) for p in range(0, 32))
		#self.promotionThreshold = kwargs.promotionThreshold if kwargs.has_key("promotionThreshold") else 2
		for bt in BTS:
			self.table[bt.weight] = [bt] + (self.table[bt.weight] if self.table.has_key(bt.weight) else [])
		self.__mutableOpReduceTable__()
	#
	def __mutableOpReduceTable__(self):
		for k in sorted(self.table.keys()):
			if len(self.table[k]) >= 2:
				(toPromote, remaining) = packByTwo(self.table[k])
				self.table[k] = remaining
				newBinomialTrees = [BinomialTree(BT1, BT2) for (BT1, BT2) in toPromote]
				self.table[2*k] = self.table[2*k] + newBinomialTrees if self.table.has_key(2*k) else newBinomialTrees


import random

L = [ random.randint(0,1000) for i in range(0,20) ]

BTS = [ BinomialTree(Node(e)) for e in L]
BH = BinomialHeap(*BTS)

[ BH.table[pow(2,p)][0].getMin() for p in range(0, 32) if len(BH.table[pow(2,p)])>0]







	