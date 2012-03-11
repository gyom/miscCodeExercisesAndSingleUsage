

scheduleData = [[0,1], [2,4], [5,6], [5.5, 5.8], [8,9], [7,8.5], [10,11], [9.5, 11.5], [12,13], [12,12.5], [13,13.5], [14,15]]

S = set(reduce(lambda acc,E: acc+E, scheduleData, []))
endpoints = [e for e in S]
endpoints.sort()

conflicts = dict( ((u,v), 0) for (u,v) in zip(endpoints[0:], endpoints[1:]))

# not very sharp algorithmically, but okay
for (a,b) in scheduleData:
	for ((u,v),n) in conflicts.items():
		if a <= u and v <= b:
			conflicts[(u,v)] = n+1


for ((u,v),n) in sorted(conflicts.items(), key = lambda ((u,v),n): u):
	if n > 1:
		print "conflict {} events in ({}, {})".format(n, u, v)