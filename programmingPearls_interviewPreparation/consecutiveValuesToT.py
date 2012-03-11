
def minimalDifference(A,B):
	
	# catching errors
	if len(A)==0 or len(B)==0:
		return None
	
	A = sorted(A)
	B = sorted(B)
	
	# initialization with first case for smoothness
	(i,j) = (0,0)
	(M,N) = (len(A), len(B))
	mindiff = float("inf")
	if A[0] <= B[0]:
		prev = A[0]
		lastread = 'a'
		i+=1
	else:
		prev = B[0]
		lastread = 'b'
		j+=1
	
	# run the while loop until both are out
	while ( i < M or j < N):
		# if they both have elements left, we need to decide from which we want to read
		if ( i < M and j < N):
			if ( A[i] <= B[j]):
				if lastread == 'b':
					mindiff = min(mindiff, A[i] - prev)
					#print "A[%d] = %d, prev = %d" % (i,A[i],prev)
				prev = A[i]
				lastread = 'a'
				#print "reading %d" % A[i] 
				i+=1
			else:
				if lastread == 'a':
					mindiff = min(mindiff, B[j] - prev)
					#print "B[%d] = %d, prev = %d" % (j,B[j],prev)
				prev = B[j]
				lastread = 'b'
				#print "reading %d" % B[j] 
				j+=1
		elif ( i < M and j >= N):
			if lastread == 'b':
				mindiff = min(mindiff, A[i] - prev)
				#print "A[%d] = %d, prev = %d" % (i,A[i],prev)
			prev = A[i]
			lastread = 'a'
			#print "reading %d" % A[i] 
			i+=1
		elif ( i >= M and j < N):
			if lastread == 'a':
				mindiff = min(mindiff, B[j] - prev)
				#print "B[%d] = %d, prev = %d" % (j,B[j],prev)
			prev = B[j]
			lastread = 'b'
			#print "reading %d" % B[j] 
			j+=1
	return mindiff

def minimalDifferenceValidator(A,B):
	if len(A)==0 or len(B)==0:
		return None
	return min([abs(a-b) for a in A for b in B])

import random
def test_minimalDifference(m=20,n=20,R=1000):
	A = [ random.randint(-R, R) for u in range(0, m)]
	B = [ random.randint(-R, R) for u in range(0, n)]
	r = minimalDifference(A,B)
	true_r = minimalDifferenceValidator(A,B)
	#print str(sorted(A))
	#print str(sorted(B))
	#print "r=%d, true_r=%d" % (r, true_r)
	assert(r == true_r)

#test_minimalDifference()
#minimalDifference([1,1,2,6,7,15], [4,4,11,20])

def cumsum(L, skipZero=False):
	if skipZero:
		R = []
	else:
		R = [0]
	acc = 0
	for e in L:
		R.append(acc+e)
		acc+=e
	return R

def findClosestSequenceSumToValue(L, targetValue):
	
	if len(L)==0:
		return float("inf")
	if len(L)==1:
		return abs(L[0]-targetValue)
	
	# L[h-1] being the last element
	(l,m,h) = (0, len(L)/2, len(L))
	
	# The two recursive calls with short circuits
	# because we know we can't get better than 0.
	# Just for fun, anticipating datasets where this happens.
	bestBefore = findClosestSequenceSumToValue(L[l:m], targetValue)
	#print "recursive call bestBefore on L[%d:%d] found %d" % (l,m, bestBefore)
	if bestBefore == 0:
		return bestBefore
	bestAfter  = findClosestSequenceSumToValue(L[m:h], targetValue)
	#print "recursive call bestAfter on L[%d:%d] found %d" % (m,h, bestAfter)
	if bestAfter == 0:
		return bestAfter
	
	cumsumBefore = cumsum(reversed(L[l:m]), skipZero=True)
	cumsumAfter  = cumsum(L[m:h], skipZero=True)
	
	# That could happen, but it should have been covered by the recursive calls
	# if that could be the situation. Anyways, adding this just in case.
	if targetValue in cumsumBefore:
		return 0
	elif targetValue in cumsumAfter:
		return 0
	
	reorganizedCumsumBefore = [u - targetValue for u in cumsumBefore]
	reorganizedCumsumAfter  = [-u for u in cumsumAfter]
	minDifferencesBetweenTheCumsums = minimalDifference(reorganizedCumsumBefore, reorganizedCumsumAfter)
	#print "minDifferencesBetweenTheCumsums got us %d" % (minDifferencesBetweenTheCumsums,)
	
	return min([bestBefore, bestAfter, minDifferencesBetweenTheCumsums])


def findClosestSequenceSumToValueValidator(L, targetValue):
	
	if len(L)==0:
		return None
	if len(L)==1:
		return abs(L[0]-targetValue)
	
	#mindiff = min([abs(u-targetValue) for u in L])
	cs = cumsum(L, skipZero=True)
	#print str(cs)
	mindiff = float("inf")
	for i in range(0, len(cs)-1):
		for j in range(i+1, len(cs)):
			# debug
			#if mindiff > abs(cs[j]-cs[i]-targetValue):
			#	print "found best sequence total between [%d,%d) : %d" % (i,j,cs[j]-cs[i])
			mindiff = min(mindiff, abs(cs[j]-cs[i]-targetValue))
	return mindiff


# findClosestSequenceSumToValueValidator([1,2,-40,23,10,23], 17)
# findClosestSequenceSumToValue([1,2,-40,23,10,23], 17)

nreps = 100
(minval, maxval) = (-100000000,100000000)
size = 1000
#for r in range(0, nreps):
for size in range(1, 1000):
	E = [random.randint(minval, maxval) for u in range(0,size)]
	target = random.randint(minval, maxval)
	result = findClosestSequenceSumToValue(E, target)
	expected = findClosestSequenceSumToValueValidator(E, target)
	print "result=%d, expected=%d" % (result, expected)
	if result != expected:
		print str(E)
		print target
	assert (result == expected)



