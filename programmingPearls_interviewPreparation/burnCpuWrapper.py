#!/usr/bin/env python

import subprocess
import math
import time
import re

nrepsInternal = 100
nreps = 10
sizes = [int(math.pow(10,u)) for u in range(6, 9)]
ops = ["exp", "log", "sqrt", "id"]
results = {}

for rep in range(0, nreps):
	for size in sizes:
		for op in ops:
			start = time.time()
			result = subprocess.check_output(["/Users/gyomalin/Documents/tmp/de_solace/tmp/entrevueGoogle/burnCpu", str(size), str(nrepsInternal), op])
			end = time.time()
			#if not re.match(("done with %s" % op), result):
			#	print("Got a failure with (rep, size, op) = (%d, %d,%s). Result was %s." % (rep, size, op, result))
			results[(rep, size, op)] = (end-start)


distilledResults = {}
for size in sizes:
	for op in ops:
		matches = [value for ((rep0, size0, op0), value) in results.items() if size0==size and op0==op]
		if len(matches) > 0:
			averageTime = sum(matches,0)/len(matches)
		else:
			averageTime = None
		# at this point we account for the fact that we ran the thing multiple times in C
		distilledResults[(size, op)] = averageTime/nrepsInternal if averageTime else None

for op in ops:
	print op
	for size in sizes:
		print "    %s : %f" % (str(size).center(15), distilledResults[(size, op)])


