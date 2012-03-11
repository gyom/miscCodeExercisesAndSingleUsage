
import random

def merge(A,B):
	R = []
	i=0;
	j=0;
	N=len(A);
	M=len(B);
	while(i+j<N+M):
		if j==M or (i<N and A[i] <= B[j]):
			R.append(A[i])
			#print "adding A[{}]={}, setting i={}".format(i, A[i], i+1)
			i=i+1
		else:
			R.append(B[j])
			#print "adding B[{}]={}, setting j={}".format(j, B[j], j+1)
			j=j+1
	return R

def partition(E,pivot):
	return ([u for u in E if u <= pivot], [u for u in E if u > pivot])


def mergesort(E):
	N = len(E)
	if N==0 or N==1:
		return E
	else:
		(A,B) = partition(E, E[random.randint(0,N-1)])
		if len(A) == 0:
			#print "We hit the special empty array condition with the other array being"
			#print B
			return merge([B[0]], mergesort(B[1:]))
		elif len(B) == 0:
			#print "We hit the special empty array condition with the other array being"
			#print A
			return merge([A[0]], mergesort(A[1:]))
		else:
			return merge(mergesort(A), mergesort(B))

niter=100
N=1000
for i in range(0, niter):
	E = [random.random() for w in range(0,N)]
	result = mergesort(E)
	reference = sorted(E)
	if not (result == reference):
		print "Error."
		print result
		print reference
		break
	else:
		print "passed round {}".format(i)
		
		
		