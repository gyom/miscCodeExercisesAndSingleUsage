
import random

def method1(income):
	if income <= 2200:
		tax = 0
	elif income <= 2700:
		tax =      0.14 * (income-2200)
	elif income <= 3200:
		tax = 70 + 0.15 * (income-2700)
	elif income <= 3700:
		tax = 145 + 0.16 * (income-3200)
	elif income <= 4200:
		tax = 225 + 0.17 * (income-3700)
	else:
		# not the point here, but let's say that the super-rich pay no taxes
		tax = 0
	return tax

def method2(income):
	categoryBase    = [0, 2200, 2700, 3200, 3700, 4200, 1000000]
	categoryTaxRate = [0, 0.14, 0.15, 0.16, 0.17,    0,       0]
	categoryOffset  = [0,    0,   70,  145,  225,    0,       0]
	
	i = 0
	while( categoryBase[i+1] <= income):
		i+=1
	# terminates when categoryBase[i] <= income < categoryBase[i+1]
	return (income - categoryBase[i])*categoryTaxRate[i] + categoryOffset[i]

if __name__ == "__main__":
	nreps = 100
	(minval, maxval) = (0, 5000)
	(okCount, errorCount) = (0, 0)
	results = {}
	for r in range(0, nreps):
		income = random.randint(minval, maxval)
		t1 = method1(income)
		t2 = method2(income)
		if (t1 == t2):
			okCount += 1
		else:
			errorCount += 1
		results[(r,income, t1, t2)] = (t1==t2)
	print "okCount = %d, errorCount = %d" % (okCount, errorCount)




