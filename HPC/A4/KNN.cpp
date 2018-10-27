#include<mpi.h>
#include<iostream>
#include<fstream>
#include<string>
#include<vector>
#include<cmath>
#include<stdlib.h>
#include<cstring>
#include<map>
#include<set>

using namespace std;

class Train_Instance {
	public:
		double r;
		double g;
		double b;
		int isSkin;
		Train_Instance(double r, double g, double b, int isSkin) {
			this->r = r;
			this->g = g;
			this->b = b;
			this->isSkin = isSkin;
		}

		double calc(double otherR, double otherG,double otherB) {
			return sqrt((r - otherR) * (r - otherR) + (g - otherG) * (g - otherG) + (b - otherB) * (b - otherB));
		}
};


class Test_Instance {
	public:
		double r;
		double g;
		double b;
		Test_Instance(double r,double g,double b) {
			this->r = r;
			this->g = g;
			this->b = b;
		}
};

vector<Train_Instance> train;
int k;

vector<string> split(string line,char a) {
 	vector<string> s;
 	string cur;
 	for(int i=0;i<line.size();i++) {
	 	if(line[i]!=a)
         	cur.push_back(line[i]);
	 	else {
		 	s.push_back(cur);
		 	cur.clear();
	 	}
 	}

 	if(cur != "")
		s.push_back(cur);
	return s;
}

int returnClassforObj(double r, double g, double b, set<double> distances, map<double,int> map_) {
   	for(int i=0;i<train.size();i++) {
	   	double dist  = train[i].calc(r,g,b);
	   	distances.insert(dist);
	   	map_.insert(std::pair<double,int>(dist,train[i].isSkin));
   	}
	int class1=0,class2=0;

	set<double>::iterator it = distances.begin();
	while(class1!=k && class2!=k) {
  		if(map_.find(*it)->second==1) class1++;
  		else if(map_.find(*it)->second==2) class2++;
  		it++;
	}
	if(class1==k)return 1;
	else if(class2==k) return 2;
}

int main() {
	
	MPI_Init(NULL,NULL);
	int size,rank;
	MPI_Comm_size(MPI_COMM_WORLD, &size);
	MPI_Comm_rank(MPI_COMM_WORLD, &rank);

	MPI_Request requests[(size - 1) * 3];
	MPI_Status statuses[(size - 1) * 3];

   	ifstream infile("training.txt");
   	if(infile.is_open()) {
	   	string line;
       	while(getline(infile,line)) {
         	vector<string> parts = split(line,' ');
         	Train_Instance instance(atof(parts[0].c_str()),atof(parts[1].c_str()),atof(parts[2].c_str()),atoi(parts[3].c_str()));
         	train.push_back(instance);
       	}
       	infile.close();
   	}
 
	//finding min and max
 	double minR = train[0].r;
 	double maxR = train[0].r;
 	double minG = train[0].g;
 	double maxG = train[0].g;
 	double minB = train[0].b;
 	double maxB = train[0].b;

	for(int i = 1; i < train.size(); i++) {
	 	minR = min(minR, train[i].r);
		maxR = max(maxR, train[i].r);

	 	minG = min(minG, train[i].g);
		maxG = max(maxG, train[i].g);

	 	minB = min(minB, train[i].b);
		maxB = max(maxB, train[i].b);
 	}
 
	//standardization
	for(int i = 0; i < train.size(); i++) {
	 	double r = (train[i].r - minR) / (maxR - minR);
 		double g = (train[i].g - minG) / (maxG - minG);
 		double b = (train[i].b - minB) / (maxB - minB);
 		train[i].r = r;
 		train[i].g = g;
 		train[i].b = b;
	}

	k = sqrt(train.size());   //assume an odd number for  2 class classification
	vector<Test_Instance> test;
	double start,end;
	if(rank == 0) {
 		ifstream file("test_.txt");
 		string newline;
 		if(file.is_open()) {
	 		while(getline(file,newline)) {
		 		vector<string> parts = split(newline, ' ');
		 		double r = atof(parts[0].c_str());
			 	double g = atof(parts[1].c_str());
		 		double b = atof(parts[2].c_str());
		 		r = (r - minR) / (maxR - minR);
		 		g = (g - minG) / (maxG - minG);
		 		b = (b - minB) / (maxB - minB);
         		Test_Instance test_(r, g, b);
         		test.push_back(test_);
	 		}
	 		file.close();
 		}

		start = MPI_Wtime();   //initial time
		int index=0;
		for(int i=1;i<test.size();i++) {
 			double r = test[i].r;
 			double g = test[i].r;
 			double b = test[i].r;	

		 	MPI_Isend(&r, 1, MPI_DOUBLE, i, 0, MPI_COMM_WORLD, requests + index); index++;
			MPI_Isend(&g, 1, MPI_DOUBLE, i, 0, MPI_COMM_WORLD, requests + index); index++;
		 	MPI_Isend(&b, 1, MPI_DOUBLE, i, 0, MPI_COMM_WORLD, requests + index); index++;  //rank=i  => no of process= no of test ex
 			//cout << "\nSent : R : " << r << " G: " << g << " B : " << b << " To " << i << " request : " << index << endl;
		}

		map<double,int> distToClass;
		set<double> distances;

		double r = test[0].r;
		double g = test[0].g;
		double b = test[0].b;
		int class_ = returnClassforObj(r, g, b, distances, distToClass);
		cout << "\nClass of 0th object is : " << class_ << endl;
	}
	else {
		double r, g, b;
		int v = (rank - 1) * 3;	
		MPI_Irecv(&r, 1, MPI_DOUBLE, 0, 0, MPI_COMM_WORLD, requests + v);   
		MPI_Irecv(&g, 1, MPI_DOUBLE, 0, 0, MPI_COMM_WORLD, requests + v + 1);
		MPI_Irecv(&b, 1, MPI_DOUBLE, 0, 0, MPI_COMM_WORLD, requests + v + 2);
		//cout << "\n--Received req+v : " << requests + v << endl;
		MPI_Wait(requests + v, statuses + v);
		MPI_Wait(requests + v + 1, statuses + v + 1);
		MPI_Wait(requests + v + 2, statuses + v + 2);

		//cout<<"\nReceived R:"<<r<<"G:"<<g<<"B:"<<b<<"to "<<rank<<endl;
		map<double,int> distToClass;
		set<double> distances;

		int class_ =  returnClassforObj(r,g,b,distances,distToClass);
		cout<<"\nClass of"<<rank<<"th object is:"<<class_<<endl;
	}

	MPI_Barrier(MPI_COMM_WORLD);
	if(rank==0) {
		end = MPI_Wtime();	
		cout<<"Elapsed time:"<<(end-start);
	}

	MPI_Finalize();
 	return 0;
}


/*

mpicxx -o hi KNN.cpp -std=c++11
mpirun -np 4 ./hi 

*/
