# 1 2 3
# 4 5 6
# 7 8 9
# . 0 .

digits = [0,1,2,3,4,5,6,7,8,9]
neighbours = {0:[4,6], 1:[6,8], 2:[7,9], 3:[4,8], 4:[3,9,0], 5:[], 6:[1,7,0], 7:[2,6], 8:[1,3], 9:[4,2]}


#[len([key for (key,S) in neighbours.items() if e in S]) for e in set(digits).difference([5])]


def generateWords(start, n, cache={}):
	if n==0:
		return []
	elif n==1:
		return [[start]]
	elif cache.has_key((start, n)):
		return cache[(start, n)]
	else:
		# actually compute the thing
		V = []
		for e in neighbours[start]:
			for rest in generateWords(e, n-1, cache):
				V.append([start] + rest)
		cache[(start, n)] = V
		return V

generateWords(1, 10)

def generateWords2(start, n, cache={}):
	if n==0:
		return []
	elif n==1:
		return [[start]]
	elif cache.has_key((start, n)):
		return cache[(start, n)]
	else:
		# actually compute the thing
		V = [[start] + rest for rest in reduce( lambda A,B:A+B, [generateWords2(w, n-1, cache) for w in neighbours[start]], [])]
		# wrong, forgets to flatten
		#V = [[start] + rest for rest in [generateWords2(w, n-1, cache) for w in neighbours[start]]]
		# bad syntax
		#V = [[start] + rest for rest in generateWords2(w, n-1, cache) for w in neighbours[start]]
		cache[(start, n)] = V
		return V

generateWords2(1, 10)




