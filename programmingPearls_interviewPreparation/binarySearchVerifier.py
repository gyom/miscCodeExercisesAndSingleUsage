
import subprocess
import random

def runTestOnce(minval, maxval, n, wantmatch):
	E = list(set([random.randint(minval, maxval) for u in range(0,n)]))
	E.sort()
	#print (minval, maxval, n, wantmatch)
	#print str(E)
	if wantmatch:
		value = E[random.randint(0,len(E)-1)]
		expectedResultForPosition = E.index(value)
	else:
		# purposefully picking an innocent value that's not in the set
		missingValues = list(set(range(minval, maxval)).difference(set(E)))
		if len(missingValues) == 0:
			print "You've set up something wrong, because all the values are in the list."
			value = -abs(minval)*2 - 1;
		else:
			value = missingValues[random.randint(0,len(missingValues)-1)]
		expectedResultForPosition = -1
	#cmdlineExpansionOfArray = str(E).replace('[', '').replace(']', '').replace(',', ' ')
	path = "/Users/gyomalin/Documents/tmp/de_solace/tmp/entrevueGoogle"
	#result = subprocess.check_output(["%s/binarySearch" % (path,), n] + E)
	#print str(["%s/binarySearch" % (path,), str(n)] + [str(e) for e in E])
	result = subprocess.check_output(["%s/binarySearch2" % (path,), str(value)] + [str(e) for e in E])
	if int(expectedResultForPosition) != int(result) :
		print "Looking for %d in %s. Got %s instead of %d" % (value, str(E), result, int(expectedResultForPosition))
	return (expectedResultForPosition, result)

if __name__ == "__main__":
	testResults = {}
	nreps = 10
	(minval, maxval) = (-100, 100)
	(okCount, errorCount) = (0, 0)
	for rep in range(0, nreps):
		for n in range(1, 100):
			wantmatch = True #random.random() > 0.5
			(expectedResultForPosition, result) = runTestOnce(minval, maxval, n, wantmatch)
			testResults[(rep, minval, maxval, wantmatch, expectedResultForPosition)] = result
			if int(expectedResultForPosition) != int(result):
				(okCount, errorCount) = (okCount, errorCount + 1)
			else:
				(okCount, errorCount) = (okCount + 1, errorCount)
	print "okCount = %s, errorCount = %s" % (okCount, errorCount)
