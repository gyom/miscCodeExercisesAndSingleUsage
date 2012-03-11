#include <stdio.h>
#include <stdlib.h>

int binarySearch(int * L, int N, int value) {
	
	if (N==0) {
		return -1;
	}
	
	/* with N being the number of elements present in L */
	int low = 0, high = N-1;
	int mid;

	while(low <= high) {
		
		//mid = (high-low)/2 + low;
		mid = (low+high)/2;
		
		if (L[mid] < value) {
			low = mid + 1;
		} else if (L[mid] > value) {
			high = mid;
			/* a potential trap
			if (high < low)
				high == low;
			*/
		} else if (L[mid] == value) {
			return mid;
		}
	}
	
	//if (L[low] == value) {
	//	return low;
	//} else {
		return -1;
	//}
}

int main ( int argc, char *argv[]) {

	if (argc >= 3) {

		// remember that argv[0] is the executable's name.
		int value = atoi(argv[1]);
		int N = argc-2;
		int * L = (int*)malloc(N*sizeof(int));
		
		int i;
		for (i=0; i<N; i++) {
			L[i] = atoi(argv[2+i]);
		}
		printf("%d", binarySearch(L,N,value));
	} else {
		printf("ERROR. Wrong number of arguments.\n");
	}

	/*
	int A0[] = {};
	int N0 = 0;

	int A1[] = {0,1,2,3,4};
	int N1 = 5;
	
	if (binarySearch(A0, N0, 42) != -1)
		printf("Failed on A0.");

	if (binarySearch(A1, N1, 2) != 2)
		printf("Failed on A1 to find 2.");

	if (binarySearch(A1, N1, 5) != -1)
		printf("Failed on A1 to find 5.");

	if (binarySearch(A1, N1, -1) != -1)
		printf("Failed on A1 to find -1.");
	*/

	return 0;
}



