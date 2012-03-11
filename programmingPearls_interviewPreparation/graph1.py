
A = {}
A[(1,2)] = 1
A[(2,4)] = 1
A[(1,4)] = 4
A[(4,5)] = 1
A[(2,5)] = 5




def nextNodes(graph, e):
	return [u for (v,u) in graph.keys() if (e == v)]

# mutates 'best' dict
def expand(graph, fringe, best):
	while len(fringe) > 0:
		newFringe = []
		for e in fringe:
			for u in nextNodes(graph,e):
				if u in best:
					if best[e] + graph[(e,u)] < best[u]:
						print "found shorter road to {} through {}".format(u, e)
						best[u] = best[e] + graph[(e,u)]
						newFringe.append(u)
					else:
						print "found bad road"
				else:
					best[u] = best[e] + graph[(e,u)]
					print "found road to {} through {}".format(u, e)
					newFringe.append(u)
			print "done with {}".format(e)
		fringe = newFringe


		
		
		
		

fringe = [1]
best = {}
best[1] = 0;

expand(A, fringe, best)





graph2 = {(1,2): 7, (2,3): 10, (2,4):15, (3,4):11, (4,5):6, (1,6):15, (1,3):9, (3,6):2, (5,6):9}
graph2.update( dict( ((v,u),c) for ((u,v),c) in graph2.items() ))
best2 = {1:0}
fringe = [1]

expand2(graph2, fringe, best2)


	
	
def expand2(graph, fringe, best):
	best = best.copy()
	for ((u,v),c) in graph.items():
		if not (u in best):
			best[u] = float("inf");
		if not (v in best):
			best[v] = float("inf");
	while len(fringe) > 0:
		newFringe = []
		for e in fringe:
			for u in nextNodes(graph,e):
				if best[e] + graph[(e,u)] < best[u]:
					best[u] = best[e] + graph[(e,u)]
					newFringe.append(u)
		fringe = newFringe
	return best



#def mergeOnMinimum(best1, best2):
#	return dict(  [(e,c) for (e,c) in best1.items() if ((e in best2) and (c < best2[e])) or not e in best2] \
#				+ [(e,c) for (e,c) in best2.items() if ((e in best1) and (c < best1[e])) or not e in best1] )

def mergeOnMinimum(best1, best2):
	return dict(  [(e,c) for (e,c) in best1.items() if (c < best2[e])] \
				+ [(e,c) for (e,c) in best2.items() if (c < best1[e])] )

def mergeFringeSets(set1, set2):
	return set(set1 + set2)

def mergePairs((best1, fringe1), (best2, fringe2)):
	return (mergeOnMinimum(best1, best2), mergeFringeSets(fringe1, fringe2))

def expandOneNode(graph, node, best):
	nextNodes = [v for (u,v) in graph.items() if (node == u)]
	nextNodesWorthExploring = [v for v in nextNodes if (best[node] + graph[(node, v)]) < best[v]]
	if len(nextNodesWorthExploring) > 0:
		reduce(mergePairs, 
		
		
		#[(best, [])] + [ ({v: best[node] + graph[(node, v)]}, if best[node] + graph[(node, v)]) for v in nextNodes])
	else:
		return best


best3 = {1: 0, 2: float("-inf"), 3: float("-inf"), 4: float("-inf"), 5: float("-inf"), 6: float("-inf")}
