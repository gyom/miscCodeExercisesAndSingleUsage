# http://finance.yahoo.com/q/hp?s=GE&a=00&b=2&c=1962&d=01&e=9&f=2012&g=d&z=66&y=66
# http://finance.yahoo.com/q/hp?s=GE&a=00&b=2&c=1962&d=01&e=9&f=2012&g=d&z=66&y=132
# http://finance.yahoo.com/q/hp?s=GE&a=00&b=2&c=1962&d=01&e=9&f=2012&g=d&z=66&y=198

import httplib
import re

# http://stackoverflow.com/questions/754593/source-of-historical-stock-data
# 	sn = TICKER
# 	a = fromMonth-1
# 	b = fromDay (two digits)
# 	c = fromYear
# 	d = toMonth-1
# 	e = toDay (two digits)
# 	f = toYear
# 	g = d for day, m for month, y for yearly

def getHistoricalStockData(quoteName, startYear, endYear, freq='d'):
	url = "/table.csv?s=%s&d=11&e=31&f=%s&g=%s&a=0&b=01&c=%s&ignore=.csv" % (quoteName, endYear, freq, startYear)
	conn = httplib.HTTPConnection("ichart.finance.yahoo.com")
	conn.request("GET",url)
	res = conn.getresponse()
	if res.status != 200:
		print res.status, res.reason
		return None
	else:
		data = res.read()
		# 1996-04-15,35.75,36.00,30.00,32.25,79219200,1.34\n
		# 1996-04-12,25.25,43.00,24.50,33.00,408720000,1.38\n
		lineRegexp = re.compile(r"^(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?)$")
		result = []
		for line in data.split("\n"):
			lineStructure = lineRegexp.match(line)
			if lineStructure:
				if lineStructure.group(1) == 'Date':
					# it's the header, so skip it
					continue
				decomposedDataForLine = {'date': lineStructure.group(1),
										 'open': float(lineStructure.group(2)),
										 'high': float(lineStructure.group(3)),
										 'low': float(lineStructure.group(4)),
										 'close': float(lineStructure.group(5)),
										 'volume': int(lineStructure.group(6)),
										 'adjclose': float(lineStructure.group(7))}
				result.append(decomposedDataForLine)
		return result

D = getHistoricalStockData("YHOO", 2005, 2012, 'm')

# conn = httplib.HTTPConnection("ichart.finance.yahoo.com")
# conn.request("GET","/table.csv?s=YHOO&d=0&e=28&f=2010&g=d&a=3&b=12&c=1996&ignore=.csv")
# res = conn.getresponse()
# print res.status, res.reason
# data = res.read()


# This whole thing is just a run-once section to distill the list of stock names from a document.

f = open('/Users/gyomalin/Dropbox/programmation/stockScraping/sp500hst.txt', 'r')
stockNameRegexp = re.compile(r"^.*?,(.*?),.*")
accum = set([])
for line in f.read().split("\n"):
	# 20091113,SAI,18.38,18.49,18.22,18.45,19189
	m = stockNameRegexp.match(line)
	if m:
		accum = accum.union([m.group(1)])
f.close()

f = open('/Users/gyomalin/Dropbox/programmation/stockScraping/allStockNames.txt', 'w')
for stockName in sorted(list(accum)):
	f.write(stockName + "\n")

f.close()

###################################################
# read the data back into Python from the file after it's been distilled

f = open('/Users/gyomalin/Dropbox/programmation/stockScraping/allStockNames.txt', 'r')
allStockNames = [name for name in f.read().split("\n") if not (name == '')]
f.close()

######################################################

pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
r = redis.Redis(connection_pool=pool)

# {'volume': 25529100, 'high': 38.19, 'adjclose': 11.9, 'low': 22.87, 'date': '2001-02-01', 'close': 23.81, 'open': 37.5},

stockName = "YHOO"
for e in getHistoricalStockData(stockName, 1950, 2012, 'd'):
	fields = ['volume', 'high', 'adjclose', 'low', 'close', 'open']
	for field in fields:
		r.set("%s:%s:%s" % (stockName, e['date'], field), e[field])
	
for stockName in allStockNames:
	D = getHistoricalStockData(stockName, 1950, 2012, 'd')
	if D:
		for e in D:
			fields = ['volume', 'high', 'adjclose', 'low', 'close', 'open']
			for field in fields:
				r.set("%s:%s:%s" % (stockName, e['date'], field), e[field])
		print "got data for %s" % (stockName, )
	else:
		print "no data for %s" % (stockName, )

# then do 51 to 524
# total estimate for size : 500 megs


stocksPopulated = []
for stockName in allStockNames:
	keysPresent = []
	for year in range(1950, 2012+1):
		for month in range(1,12+1):
			for day in range(1,31+1):
				key = "%s:%d-%0.2d-%0.2d:%s" % (stockName, year, month, day, "close")
				if r.get(key):
					keysPresent.append("%d-%0.2d-%0.2d" % (year, month, day))
	if len(keysPresent) > 0:
		stocksPopulated.append(stockName)
		S = sorted(keysPresent)
		start = S[0]
		end = S[-1]
		r.set("delimiters:start:%s" % (stockName, ), start)
		r.set("delimiters:end:%s" % (stockName, ), end)
		print "%s goes from %s to %s" % (stockName, start, end)

#
for stockName in stocksPopulated:
	r.rpush("allStockNames", stockName)

################################################
#
def generateDatesInAYear(year):
	days = {}
	days['01'] = range(1,31+1)
	if (year % 4 == 0):
		days['02'] = range(1,29+1)
	else:
		days['02'] = range(1,28+1)
	days['03'] = range(1,31+1)
	days['04'] = range(1,30+1)
	days['05'] = range(1,31+1)
	days['06'] = range(1,30+1)
	days['07'] = range(1,31+1)
	days['08'] = range(1,31+1)
	days['09'] = range(1,30+1)
	days['10'] = range(1,31+1)
	days['11'] = range(1,30+1)
	days['12'] = range(1,31+1)
	months = ["%0.2d" % m for m in range(1,13)]
	return [ ("%0.4d-%s-%0.2d" % (year, month, day)) for month in months for day in days[month] ]


# populate the redis server with that so as to never have to compute those values again
for year in range(1950,2020):
	for date in generateDatesInAYear(year):
		r.rpush("allDatesInYear:%0.4d" % year, date)
#
# A = r.lrange("allDatesInYear:1970", 0, -1)



#######################
#
# To get back on your feed from nothing, you get the list like this.
allStockNames = r.lrange("allStockNames", 0, -1)

# from numpy import *

def timeIntervalOfQuote(stockName):
	start = r.get("delimiters:start:%s" % (stockName, ))
	end   = r.get("delimiters:end:%s" % (stockName, ))
	if (not start) or (not end):
		return None
	#startYear = int(re.match(r".*?:(\d*?)-.*?:", start).group(1))
	#endYear   = int(re.match(r".*?:(\d*?)-.*?:", end  ).group(1))
	startYear = int(re.match(r"(\d*?)-.*?", start).group(1))
	endYear   = int(re.match(r"(\d*?)-.*?", end  ).group(1))
	return {"start": start, "end": end, "startYear":startYear, "endYear":endYear}

#def makeNumpyArrayFromQuote(stockName, fieldName="close"):
#	I = timeIntervalOfQuote(stockName)
#	startYear = I['startYear']
#	endYear   = I['endYear']
#	prices = []
#	for year in range(startYear, endYear+1):
#		for month in range(1,12+1):
#			for day in range(1,31+1):
#				key = "%s:%d-%0.2d-%0.2d:%s" % (stockName, year, month, day, fieldName)
#				v = r.get(key)
#				print v
#				if v:
#					prices.append(float(v))
#	return numpy.array(prices)

#  AAPL = makeNumpyArrayFromQuote("AAPL")
#  XRX  = makeNumpyArrayFromQuote("XRX")

#  Write something to get a number of stocks between start and end as a numpy array / matrix.
#
#  retrieveStockBlock(stockNameList, start, end, fieldName="close")
#     --> a numpy array of size (M, N)
#  where M = len(stockNameList)
#  and   N = however many days there are between start and end

def retrieveStockBlock(redisConn, stockNameList, start, end, fieldName="close", queryCombinationThreshold=0, useNan=True):
	
	startYear = int(re.match(r"(\d*?)-.*?", start).group(1))
	endYear   = int(re.match(r"(\d*?)-.*?", end  ).group(1))
	
	interwovenPricesAccumulator = []
	queries = []
	
	for year in range(startYear, endYear+1):
		for date in r.lrange("allDatesInYear:%0.4d" % year, 0, -1):
			if start <= date and date <= end:
				for stockName in stockNameList:
					queries.append("%s:%s:%s" % (stockName, date, fieldName))
					if len(queries) > queryCombinationThreshold:
						prices = redisConn.mget(queries)
						if useNan:
							interwovenPricesAccumulator.extend( [float(p) if p else numpy.NAN for p in prices ] )
						else:
							interwovenPricesAccumulator.extend( [float(p) if p else p for p in prices ])
						queries = []
	if len(queries) > 0:
		# some are left
		prices = redisConn.mget(queries)
		if useNan:
			interwovenPricesAccumulator.extend( [float(p) if p else numpy.NAN for p in prices ] )
		else:
			interwovenPricesAccumulator.extend( [float(p) if p else p for p in prices ])
	
	interwovenPrices = numpy.array(interwovenPricesAccumulator)
	# We have to spin the array just a bit to put it as we want.
	# This would have been avoided if we hadn't queried the stock prices
	# in that order with all the companies grouped.
	(M,N) = (len(stockNameList), interwovenPrices.shape[0]/len(stockNameList))
	interwovenPrices = numpy.reshape(interwovenPrices, (N,M))
	return interwovenPrices.transpose()

L = retrieveStockBlock(r, ["AAPL", "GOOG", "YHOO"], "2010-01-01", "2010-02-10")

def shortDiscreteConvolution(dataMatrix, filterCoefficients, filterOffsetRange, wantNormalization=True):
	# dataMatrix = matrix of dimensions  companies x pricesInTime
	# filterCoefficients = [0.1, 0.2, 0.3, 0.2, 0.1]
	# filterOffsetRange  = [-2,-1,0,1,2]
	
	(M,N) = dataMatrix.shape
	
	d = max([abs(c) for c in filterOffsetRange])
	paddedDataMatrix = numpy.hstack( (numpy.zeros( (M, d)), dataMatrix, numpy.zeros( (M, d))) )
	
	convolutionAccumulator = numpy.zeros( paddedDataMatrix.shape )
	normalizationWeights    = numpy.zeros( paddedDataMatrix.shape )
	
	# the continuous pixel split trick where we account for the weights sent to
	# every target pixel when doing the translations
	holes = numpy.isnan(paddedDataMatrix)
	patchedPaddedDataMatrix = numpy.where(holes, numpy.zeros( paddedDataMatrix.shape ), paddedDataMatrix)
	# patchedPaddedWeights[i,j] = 1 iff the original data was present at (i,j) and was not nan.
	# Otherwise, patchedPaddedWeights[i,j] = 0.
	patchedPaddedWeights    = numpy.where(holes, numpy.zeros( paddedDataMatrix.shape ),
												 numpy.hstack(( numpy.zeros( (M, d)),
																numpy.ones(  dataMatrix.shape),
																numpy.zeros( (M, d))) ) )
	
	for os in filterOffsetRange:
		#print "d=%d, N=%d, os=%d" % (d, N, os)
		convolutionAccumulator[:,d:(N+d)] += patchedPaddedDataMatrix[:,(d+os):(N+d+os)] * filterCoefficients[os]
		normalizationWeights[  :,d:(N+d)] += patchedPaddedWeights[   :,(d+os):(N+d+os)] * filterCoefficients[os]
	
	if wantNormalization:
		return numpy.where(normalizationWeights[:,d:(N+d)] <= 0, numpy.zeros((M,N)), convolutionAccumulator[:,d:(N+d)] / normalizationWeights[:,d:(N+d)] )
	else:
		return convolutionAccumulator[:,d:(N+d)]


# dataMatrix = numpy.array([[10,20,30], [100,200,300]])
# filterCoefficients = numpy.array([1, 0.5])
# filterOffsetRange  = numpy.array([0, 1])
# R = shortDiscreteConvolution(dataMatrix, filterCoefficients, filterOffsetRange)


L = retrieveStockBlock(r, ["AAPL", "GOOG", "YHOO"], "2000-01-01", "2009-12-31")
osr = numpy.arange(-50,50+1)
osc = numpy.exp(-numpy.abs(osr))
S = shortDiscreteConvolution(L, osc, osr)

# x1 = numpy.arange(0,S.shape[1])
# y1 = numpy.array(S[0,:])
# pylab.plot(x1,y1)
# x2 = numpy.arange(0,L.shape[1])
# y2 = numpy.array(L[0,:])
# pylab.plot(x2,y2)
# pylab.show()

def differentiateFromPreviousInTime(stockDataMatrix):
	delta = stockDataMatrix[:,1:] - stockDataMatrix[:,0:-1]
	return numpy.hstack( (delta[:,0:1], delta) )

dS  = differentiateFromPreviousInTime(S)
ddS = differentiateFromPreviousInTime(dS)


def extrapolateWithDerivatives(S, t):
	dS  = differentiateFromPreviousInTime(S)
	ddS = differentiateFromPreviousInTime(dS)
	return S + t*dS + 0.5*t*t*ddS

t=1
stock=2
pred = extrapolateWithDerivatives(S,t)
diff = pred[stock,2:-t] - L[stock,2+t:]
pylab.plot(diff)
pylab.show()

