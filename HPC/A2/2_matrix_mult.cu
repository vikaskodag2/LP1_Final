#include<cuda.h>
#include<stdio.h>

int main(void) {
    void MatrixMultiplication(float *, float *, float *, int,int,int);
    const int k =5 ;
    const int m=4,n=3;

    float M[k*n], N[n*m], P[k*m];
    for(int i = 0; i < (k*n) ; i++) {
        M[i] = 6;

    }
    for(int i = 0; i < (n*m) ; i++) {
            //M[i] = 6;
            N[i] = 6;
           // P[i] = 0;
        }
    for(int i = 0; i < (k*m) ; i++) {
            //M[i] = 6;
           // N[i] = 6;
            P[i] = 0;
        }
    MatrixMultiplication(M, N, P,m,n,k);
    for(int i = 0; i < (k*m) ; i++) {
        printf("%f \n", P[i]);
    }
    int quit;
    scanf("%d",&quit);
    return 0;
}

//Matrix multiplication kernel - thread specification
__global__ void MatrixMulKernel(float *Md, float *Nd, float *Pd, int N,int M) {
    //2D Thread ID
    int tx = threadIdx.x;
    int ty = threadIdx.y;
    printf("%d %d\n",tx,ty);
    //Pvalue stores the Pd element that is computed by the thread
    float Pvalue = 0;

    for(int k = 0; k <N ; ++k) {
        float Mdelement = Md[tx*N + k];
        float Ndelement = Nd[k*M + ty];
        Pvalue += (Mdelement*Ndelement);
    }

    Pd[tx*M + ty] = Pvalue;
}

void MatrixMultiplication(float *M, float *N, float *P, int m,int n,int k) {
    //int size = Width*Width*sizeof(float);
    float *Md, *Nd, *Pd;

    //Transfer M and N to device memory
    cudaMalloc((void**)&Md, k*n*sizeof(float));
    cudaMemcpy(Md,M,k*n*sizeof(float),cudaMemcpyHostToDevice);
    cudaMalloc((void**)&Nd, n*m*sizeof(float));
    cudaMemcpy(Nd,N,n*m*sizeof(float),cudaMemcpyHostToDevice);

    //Allocate P on the device
    cudaMalloc((void**)&Pd,k*m*sizeof(float));

    //Setup the execution configuration
    dim3 dimBlock(k,m);
    dim3 dimGrid(1,1);

    //Launch the device computation threads!
    MatrixMulKernel<<<dimGrid,dimBlock>>>(Md,Nd,Pd,n,m);

    //Transfer P from device to host
    cudaMemcpy(P,Pd,m*k*sizeof(float),cudaMemcpyDeviceToHost);

    //Free device matrices
    cudaFree(Md);
    cudaFree(Nd);
    cudaFree(Pd);
}

