#Open ipython notebook
import pandas as pd
import numpy as np
from sklearn import preprocessing, model_selection,neighbors

df = pd.read_csv('2010-capitalbikeshare-tripdata.csv')
#print(df.head())
df.drop(['Bike number'],1,inplace=True)
df.convert_objects(convert_numeric=True)

def handle_non_numerical_data(df):
    columns = df.columns.values

    for column in columns:
        text_digit_vals = {}
        def convert_to_int(val):
            return text_digit_vals[val]

        if df[column].dtype != np.int64 and df[column].dtype != np.float64:
            column_contents = df[column].values.tolist()
            unique_elements = set(column_contents)
            x = 0
            for unique in unique_elements:
                if unique not in text_digit_vals:
                    text_digit_vals[unique] = x
                    x+=1

            df[column] = list(map(convert_to_int, df[column]))

    return df

df = handle_non_numerical_data(df)

x = np.array(df.drop(['Member type'],1))
y = np.array(df['Member type'])

x_train, x_test, y_train, y_test = model_selection.train_test_split(x,y,test_size=0.2)

knn = neighbors.KNeighborsClassifier()
knn.fit(x_train, y_train) 

accuracy = knn.score(x_test,y_test)
print(accuracy)
#knn.predict([[1959,56816,13751,31200,73,31108,69,935]])

example_measures = np.array([[1959,56816,13751,31200,73,31108,69]])
example_measures = example_measures.reshape(1,-1)
prediction = knn.predict(example_measures)
print(prediction)


