#include <omp.h>
#include <stdio.h>
#include <stdlib.h>

void swap();

int main (int argc, char *argv[]) {

	int A[5] = {6,9,1,3,7};
	int N = 5;
	int i=0, j=0; 
	int first;

	for( i = 0; i < N; i++ )
	{
		first = i % 2; 
		#pragma omp parallel for default(none),shared(A,first,N)
		for( j = first; j < N-1; j += 2 )
		{
			if( A[ j ] > A[ j+1 ] )
			{
				swap( &A[ j ], &A[ j+1 ] );
			}
		}
	}

	for(i=0;i<N;i++)
	{
		printf("\n %d",A[i]);
	}
}

void swap(int *num1, int *num2)
{

	int temp = *num1;
	*num1 =  *num2;
	*num2 = temp;
}



/*
OUTPUT:

[ccoew@localhost 4423]$ gcc -fopenmp bubble.c
[ccoew@localhost 4423]$ ./a.out

 1
 3
 6
 7
 9
*/

