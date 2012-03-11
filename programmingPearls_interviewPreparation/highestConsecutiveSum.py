
def highestConsecutiveSum(E):
	n = len(E)
	if n==0:
		return 0
	P = [0 for i in range(0, n)]
	P[0] = E[0]
	for i in range(1,n):
		P[i] = E[i] + max(0, P[i-1])
	
	Q = [0 for i in range(0, n)]
	Q[n-1] = E[n-1]
	for i in reversed(range(0,n-1)):
		Q[i] = E[i] + max(0, Q[i+1])
	
	S = [0 for i in range(0, n)]
	for i in range(0,n-1):
		S[i] = max(0, P[i]) + max(0, Q[i+1])
	S[n-1] = max(0, P[n-1])
		
	return max(S)

highestConsecutiveSum([31, -41, 59, 26, -53, 58, 97, -93, -23, 84])
