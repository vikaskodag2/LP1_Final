import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn import metrics
from sklearn.model_selection import KFold

diabetes_dataset = pd.read_csv("diabetes.csv")
# print(diabetes_dataset.groupby("Outcome").size())
dataset_nozeros = diabetes_dataset.copy()
zero_fields = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI'] 
diabetes_dataset[zero_fields] = diabetes_dataset[zero_fields].replace(0, np.nan)
diabetes_dataset[zero_fields] = diabetes_dataset[zero_fields].fillna(dataset_nozeros.mean())
# print(diabetes_dataset.describe())

# Data Stratification
# When we split the dataset into train and test datasets, the split is completely random. Thus the instances of each class label or outcome in the train or test datasets is random. Thus we may have many instances of class 1 in training data and less instances of class 2 in the training data. So during classification, we may have accurate predictions for class1 but not for class2. Thus we stratify the data, so that we have proportionate data for all the classes in both the training and testing data.

train,test = train_test_split(diabetes_dataset, test_size=0.25, random_state=0, stratify=diabetes_dataset['Outcome'])
train_X = train[train.columns[:8]]
test_X = test[test.columns[:8]]
train_Y = train['Outcome']
test_Y = test['Outcome']

model = GaussianNB()

model.fit(train_X,train_Y)
prediction = model.predict(test_X)

accuracy = (metrics.accuracy_score(test_Y, prediction))
print("Accuracy : %s" % "{0:.5%}".format(accuracy))

kf = KFold(n_splits=5)
kf.get_n_splits(train_X)
error = []
for train, test in kf.split(train_X, train_Y) :
	train_predictors = (train_X.iloc[train,:])
	train_target = train_Y.iloc[train]
	model.fit(train_predictors, train_target)
	error.append(model.score(train_X.iloc[test, :], train_Y.iloc[test]))
	print("Cross-Validation Score : %s" % "{0:.5%}".format(np.mean(error)))


confusion_matrix = metrics.confusion_matrix(test_Y, prediction)
print(confusion_matrix)

TP = confusion_matrix[1, 1]
TN = confusion_matrix[0, 0]
FP = confusion_matrix[0, 1]
FN = confusion_matrix[1, 0]





















