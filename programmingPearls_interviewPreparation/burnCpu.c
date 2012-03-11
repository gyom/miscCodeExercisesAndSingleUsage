#include <stdio.h>
#include <stdlib.h>
#include <math.h>

void idOnArray(double * E, long N) {
	long i=0;
	for(i=0; i<N;++i) {
		E[i] = E[i];
	}
	return;
}

void sqrtOnArray(double * E, long N) {
	long i=0;
	for(i=0; i<N;++i) {
		E[i] = sqrt(E[i]);
	}
	return;
}

void logOnArray(double * E, long N) {
	long i=0;
	for(i=0; i<N;++i) {
		E[i] = log(E[i]);
	}
	return;
}

void exponentialOnArray(double * E, long N) {
	long i=0;
	for(i=0; i<N;++i) {
		E[i] = exp(E[i]);
	}
	return;
}

void resetArray(double * E, long N) {
	long i=0;
	for(i=0; i<N;++i) {
		E[i] = (double)i;
	}
}

int main(int argc, char *argv[]) {
	/*
		burnCpu   niter   fname
	*/

	if (argc < 4) {
		printf("We need two arguments :  size  niter  fname \n");
		return 1;
	}

	long N = atol(argv[1]);
	if (N<=0) {
		printf("size has to be positive.");
	}

	long niter = atol(argv[2]);
	if (niter<=0) {
		printf("niter has to be positive.");
	}

	double * E = (double*)malloc(sizeof(double)*N);
	resetArray(E, N);
	
	char * fname = argv[3];
	
	int r=0;
	if (strcmp(fname, "exp") == 0) {
		for(r=0; r<niter;++r) {
			resetArray(E, N);
			exponentialOnArray(E, N);
		}
		printf("done with exp\n");
	} else if (strcmp(fname, "log") == 0) {
		for(r=0; r<niter;++r) {
			resetArray(E, N);
			logOnArray(E, N);
		}
		printf("done with log\n");
	} else if (strcmp(fname, "sqrt") == 0) {
		for(r=0; r<niter;++r) {
			resetArray(E, N);
			sqrtOnArray(E, N);
		}
		printf("done with sqrt\n");
	} else if (strcmp(fname, "id") == 0) {
		for(r=0; r<niter;++r) {
			resetArray(E, N);
			idOnArray(E, N);
		}
		printf("done with id\n");
	} else {
		printf("nothing done\n");
	}

	return 0;
}

/*

szkmtk-mba:entrevueGoogle gyomalin$ python burnCpuWrapper.py 

exp
        1000000     : 0.011482
        10000000    : 0.114639
       100000000    : 1.176501
log
        1000000     : 0.022984
        10000000    : 0.230018
       100000000    : 2.310665
sqrt
        1000000     : 0.011671
        10000000    : 0.115764
       100000000    : 1.158500
id
        1000000     : 0.006451
        10000000    : 0.063060
       100000000    : 0.631304

*/
