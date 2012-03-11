
C[(i,j)] = 
	0                        if i==0 or j==0
	C[(i-1,j-1)] + 1         if A[i] == B[j]
	max(C[i-1,j], C[i, j-1]) otherwise
	

A = "absdsbebnfjdsfdbsnabd"
B = "asdjbabsbrbebdssbb"
	
C = dict(  [((i,-1), 0) for i in range(-1, len(A))] + [((-1,j), 0) for j in range(-1, len(B))] )

for i in range(0, len(A)):
	for j in range(0, len(B)):
		C[(i,j)] = C[(i-1, j-1)] + 1 if A[i] == B[j] else max( C[(i-1,j)], C[(i,j-1)])


################################################		
		
# eurque ! marche tout croche, doit etre revu

D = ""
i=0
j=0

while i < len(A) and j < len(B):
	if C[(i,j)] == C[(i-1,j-1)] + 1:
		D = D + A[i]
		print "appending {} to solution at ({},{})".format(A[i],i,j)
		i=i+1
		j=j+1
	elif C[(i,j)] == C[(i,j-1)] and j + 1 < len(B):
		print "advancing j because C[({},{})] == C[({},{})]".format(i,j,i,j-1)
		j=j+1
	elif C[(i,j)] == C[(i-1,j)] and i + 1 < len(A):
		print "advancing i because C[({},{})] == C[({},{})]".format(i,j,i-1,j)
		i=i+1
	else:
		print "something is wrong"

################################################		
	

	


	