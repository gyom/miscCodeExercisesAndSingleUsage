
import math
import numpy
import pylab

def averageIndices(s, T):
	low = int(math.floor(s))
	high = int(math.ceil(s))
	if (low==high):
		return T[low]
	else:
		dlow = abs(s-low)
		dhigh= abs(s-high)
		return dhigh/(dlow+dhigh)*T[low] + dlow/(dlow+dhigh)*T[high]

N = 10000000
startOffset = 1
T = [u for u in range(0,startOffset)] + [0 for u in range(0,N-startOffset)]

for n in range(startOffset,N):
	s = math.sqrt(n)
	T[n] = 6*n + 3*s*averageIndices(s, T)


x = numpy.arange(0,N)
y = numpy.array(T)
pylab.plot(x,y)
pylab.show()

nlogn    = numpy.array([1 for u in range(0,5)] + [u*math.log(u) for u in range (5,N)])
nloglogn = numpy.array([1 for u in range(0,5)] + [u*math.log(math.log(u)) for u in range (5,N)])

y_ratio = y / nlogn
y_ratio2 = y / nloglogn

#pylab.plot(x,y_ratio)
#pylab.plot(x,y_ratio2)

