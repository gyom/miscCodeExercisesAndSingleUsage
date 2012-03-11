
# writing again by heart the program from Norvig, 2012-01-15

def cross(A,B):
	return [a+b for a in A for b in B]

digits = '123456789'
rows = 'ABCDEFGHI'
cols = digits

squares = cross(rows, cols)
unitlist = [cross(a,cols) for a in rows] + [cross(rows, [b]) for b in cols] + [cross(A,B) for A in ['ABC', 'DEF', 'GHI'] for B in ['123', '456', '789']]


units = dict( (s, [u for u in unitlist if s in u] ) for s in squares )
#dict( (s, [u for u in [[1,2], [1,3], [2,3]] if s in u]) for s in [1,2,3])
#dict( (s, [u for u in [['A1','B2'], ['A1','C3'], ['B2','C3']] if s in u]) for s in ['A1','B2','C3', 'D4'])

peers = dict( (s, set(sum(units[s],[])) - set([s]) ) for s in squares )


def display(values):
	str = ""
	for s in squares:
		if len(values[s]) == 0:
			str = str + " X "
		elif len(values[s]) == 1:
			str = str + " " + values[s] + " "
		else:
			str = str + " . "
		if s == "C9":
			str = str + "\n"
			str = str + "----------------------------"
			str = str + "\n"
		elif s == "F9":
			str = str + "\n"
			str = str + "----------------------------"
			str = str + "\n"
		elif '3' in s or '6' in s:
			str = str + " | "
		elif '9' in s:
			str = str + "\n"
	print str


def grid_values(grid):
	V = [c for c in grid if c in digits or c in '0.']
	return dict(zip(squares, V))

def parse_grid(grid):
	values = dict( (s, digits) for s in squares)
	for k,v in grid_values(grid).items():
		#print "processing location {} with value {}".format(k, v)
		if v in digits and not assign(values, k, v):
			print "failed to assign location {} value {} ".format(k, v)
			return False
	return values


def assign(values, k, v):
	if v in values[k]:
		values[k] = v
		for p in peers[k]:
			# eliminate the value, but now continue if that means that
			# that square has only one value left
			if eliminate(values, p, v) and len(values[p]) == 1:
				# assign that value, but return a general failure if that
				# assignment led to a contradiction
				if not assign(values, p, values[p]):
					return False
		return values
	else:
		# tried to assign an illegal value
		return False

def eliminate(values, k, v):
	if v in values[k]:
		values[k] = values[k].replace(v, '')
		# return True if we indeed took out a value
		return True
	else:
		# return False if it was already eliminated (like usual)
		return False










grid1 = '003020600900305001001806400008102900700000008006708200002609500800203009005010300'
display(parse_grid(grid1))
# 4  8  3  |  9  2  1  |  6  5  7
# 9  6  7  |  3  4  5  |  8  2  1
# 2  5  1  |  8  7  6  |  4  9  3
#----------------------------
# 5  4  8  |  1  3  2  |  9  7  6
# 7  2  9  |  5  6  4  |  1  3  8
# 1  3  6  |  7  9  8  |  2  4  5
#----------------------------
# 3  7  2  |  6  8  9  |  5  1  4
# 8  1  4  |  2  5  3  |  7  6  9
# 6  9  5  |  4  1  7  |  3  8  2


			
			

grid2 = """
4 . . | . . . | 8 . 5
. 3 . | . . . | . . .
. . . | 7 . . | . . .
---------------------
. 2 . | . . . | . 6 .
. . . | . 8 . | 4 . . 
. . . | . 1 . | . . . 
---------------------
. . . | 6 . 3 | . 7 .
5 . . | 2 . . | . . . 
1 . 4 | . . . | . . . 
"""

A = parse_grid(grid2)
display(A)

# won't solve the thing






