#Import Library of Gaussian Naive Bayes model
import sklearn.metrics
from sklearn.naive_bayes import GaussianNB
import numpy as np
import math
import random

data = np.loadtxt('pima-indians-diabetes.csv', delimiter = ',')
X_train = data[0:667,0:8]
Y_train = data[0:667,8:9]
X_test = data[667:767,0:8]
Y_test = data[667:767,8:9]
arr1 = np.array(X_train, np.float32)
arr2 = np.array(Y_train, np.float32)
##Create a Gaussian Classifier
model = GaussianNB()

# Train the model using the training sets 
model.fit(arr1,arr2.ravel())
#Predict Output 
predicted= model.predict(X_test)
score = sklearn.metrics.accuracy_score(Y_test, predicted, normalize=True, sample_weight=None)*100
print (predicted)
print (score)
