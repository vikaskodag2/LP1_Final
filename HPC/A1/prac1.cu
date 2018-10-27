#include "cuda_runtime.h"
#include "device_launch_parameters.h"
#include<stdio.h>
#include<stdlib.h>
#include<time.h>
#include<math.h>

void init_array(float *a,int n);

__global__
void sum(float* input)
{
	int tid=threadIdx.x;
	int no_threads=blockDim.x;
	int step_size=1;
	
	while(no_threads>0)
	{
		 //printf("\n tid:%d  no_threads:%d  step_size:%d \n",tid,no_threads,step_size);
		 if(tid<no_threads)
		 {
		 	int fst=tid*step_size*2;
		 	int snd=fst+step_size;
		 	input[fst]+=input[snd];
		 }
		 step_size <<= 1;
		 no_threads >>=1;
	}
}

__global__
void max(float* input)
{
	int tid=threadIdx.x;
	int no_threads=blockDim.x;
	int step_size=1;
	
	while(no_threads>0)
	{
		if(tid<no_threads)
		{
			int fst=tid*step_size*2;
			int snd=fst+step_size;
			if(input[fst]<input[snd])
				input[fst]=input[snd];
		}
		step_size <<= 1;
		no_threads >>=1;
	}
}
 
__global__
void min(float* input)
{
	int tid=threadIdx.x;
	int no_threads=blockDim.x;
	int step_size=1;
	
	while(no_threads>0)
	{
		if(tid<no_threads)
		{
			int fst=tid*step_size*2;
			int snd=fst+step_size;
			if(input[fst]>input[snd])
				input[fst]=input[snd];
		}
		step_size <<= 1;
		no_threads >>=1;
	}
}

__global__
void std_(float* input,float avg)
{
	int tid=threadIdx.x;
	int no_threads=blockDim.x;
	int step_size=1;
	
	while(no_threads>0)
	{
		if(tid<no_threads)
		{
			int fst=tid*step_size*2;
			int snd=fst+step_size;
			if(step_size==1){
			input[fst] = (input[fst]-avg)*(input[fst]-avg);
      			input[snd] = (input[snd]-avg)*(input[snd]-avg);
      			input[fst] += input[snd];}
      			else{
      			input[fst] += input[snd];
      			}
		}
		step_size <<= 1;
		no_threads >>=1;
	}
}




int main()
{
	int n=4;
	float *a,*d_a;
	float SUM,MAX,MIN,STD_,avg;
	a=(float*)malloc(sizeof(float)*n);
	cudaMalloc(&d_a,n*sizeof(float));
	init_array(a,n);
	for(int i=0;i<n;i++)
		printf("%f   ",a[i]);
	float m;
	
	
	
	
//	for(int i=0;i<n;i++)  //sequential sum
//		m=m+a[i];

/**********************************************************************************************/
	cudaMemcpy(d_a,a,n*sizeof(float),cudaMemcpyHostToDevice);
	sum<<<1,n/2>>>(d_a);
	cudaMemcpy(&SUM,d_a,sizeof(float),cudaMemcpyDeviceToHost);
	printf("SUM:%f",SUM);
/**********************************************************************************************/


/**********************************************************************************************/
	cudaMemcpy(d_a,a,n*sizeof(float),cudaMemcpyHostToDevice);
	max<<<1,n/2>>>(d_a);
	cudaMemcpy(&MAX,d_a,sizeof(float),cudaMemcpyDeviceToHost);
	printf("\nMax:%f",MAX);
/**********************************************************************************************/


/**********************************************************************************************/
	cudaMemcpy(d_a,a,n*sizeof(float),cudaMemcpyHostToDevice);
	min<<<1,n/2>>>(d_a);
	cudaMemcpy(&MIN,d_a,sizeof(float),cudaMemcpyDeviceToHost);
	printf("\nMin:%f",MIN);
/**********************************************************************************************/


/**********************************************************************************************/
	avg=SUM/n;
	cudaMemcpy(d_a,a,n*sizeof(float),cudaMemcpyHostToDevice);
	std_<<<1,n/2>>>(d_a,avg);
	cudaMemcpy(&STD_,d_a,sizeof(float),cudaMemcpyDeviceToHost);
	STD_ = STD_/n;
	STD_ = sqrt(STD_);
	printf("\nSTD:%f",STD_);
/**********************************************************************************************/

	cudaFree(d_a);
	delete[] a;
	return 0;
}

void init_array(float*a,int n)
{
  for(int i=0;i<n;i++)
     a[i] = rand()%n + 1;
}
