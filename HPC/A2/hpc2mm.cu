#include<stdio.h>
#include<stdlib.h>

__global__ void kernel(float* da,float* db,float* dc,int n)
{
    int tx=threadIdx.x;
    int ty=threadIdx.y;
    int sum=0;

    for(int i=0;i<n;i++)
    {
        sum =sum + da[tx*n+i]*db[i*n+ty];
    }
    dc[tx*n+ty]=sum;
    
}
void init(float* a,int n)
{
    for(int i=0;i<n;i++)
    {
        for(int j=0;j<n;j++)
        {
            a[i*n+j]=rand%n+1;
        }
    }
}

void printm(float *a,int n)
{
    for(int i=0;i<n;i++)
    {
        for(int j=0;j<n;j++)
        {
            printf(" %f",a[i*n+j]);
        }
        printf("\n");
    }
}

int main()
{
float *a,*b,*c;
float *da,*db,*dc;

int n;
n=3;


a=(float*)malloc(sizeof(float)*n*n);
b=(float*)malloc(sizeof(float)*n*n);
c=(float*)malloc(sizeof(float)*n*n);

init(a,n);
init(b,n);

printm(a,n);
printm(b,n);


cudaMalloc(&da,sizeof(float)*n*n);
cudaMalloc(&dc,sizeof(float)*n*n);
cudaMalloc(&db,sizeof(float)*n*n);

cudaMemcpy(da,a,sizeof(float)*n*n,cudaMemcpyHostToDevice);
cudaMemcpy(db,b,sizeof(float)*n*n,cudaMemcpyHostToDevice);

dim3 dimGrid(1,1);
dim3 dimBlock(n,n);


kernel<<<dimGrid,dimBlock>>>(da,db,dc,n);

cudaMemcpy(c,dc,sizeof(float)*n*n,cudaMemcpyDeviceToHost);
printm(c,n);

cudaFree(da);
cudaFree(db);
cudaFree(dc);

delete[] a;
delete[] b;
delete[] c;	
	
	
return 0;
}
