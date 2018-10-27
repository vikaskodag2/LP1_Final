#include <iostream>

using namespace std;

__global__ void multiply(int *ad, int *bd, int *cd, int n)
{

	int row = blockIdx.x ;
	int col = blockIdx.y ;

	int sum = 0;

	for (int i = 0; i < n; i++)

	{
		sum = sum + ad[row * n + i] * bd[i * n + col];
	}

	cd[row * n + col] = sum;
}

int main()
{

	cout << "Enter the size" << endl;
	int n;

	cin >> n;

	int a[n * n], b[n * n], c[n * n];

	for (int i = 0; i < n; i++)
	{

		for (int j = 0; j < n; j++)

		{

			a[i * n + j] = i;
			b[i * n + j] = i;
		}
	}
for (int i = 0; i < n; i++)
	{

		for (int j = 0; j < n; j++)
		{

			cout << a[i * n + j] << " ";
		}
		cout << endl;
	}
	int size = n * n * sizeof(int);

	int *ad, *bd, *cd;

	cudaEvent_t start, end;

	cudaMalloc(&ad, size);
	cudaMemcpy(ad, a, size, cudaMemcpyHostToDevice);

	cudaMalloc(&bd, size);
	cudaMemcpy(bd, b, size, cudaMemcpyHostToDevice);

	cudaMalloc(&cd, size);

	dim3 grid(n, n, 1);
	dim3 block(1, 1, 1);

	cudaEventCreate(&start);
	cudaEventCreate(&end);

	cudaEventRecord(start);

	multiply<<<grid, block>>>(ad, bd, cd, n);

	cudaEventRecord(end);
	cudaEventSynchronize(end);

	float time = 0;

	cudaEventElapsedTime(&time, start, end);

	cudaMemcpy(c, cd, size, cudaMemcpyDeviceToHost);

	for (int i = 0; i < n; i++)
	{

		for (int j = 0; j < n; j++)
		{

			cout << c[i * n + j] << " ";
		}
		cout << endl;
	}

	cout << "The time required is " << time << endl;
}
