import numpy as np # linear algebra
import pandas as pd
import matplotlib.pyplot as plt

iris=pd.read_csv('iris.csv')

#as seenn in the above id is not useful in the plotting of data,so drop that coloumn 
iris=iris.drop('Id',axis=1)

print(iris.describe())
print(iris['Species'].value_counts())


setosa=iris[iris['Species']=='Iris-setosa']
versicolor =iris[iris['Species']=='Iris-versicolor']
virginica =iris[iris['Species']=='Iris-virginica']

plt.figure()
fig,ax=plt.subplots(1,2,figsize=(21, 10))

setosa.plot(x="SepalLengthCm", y="SepalWidthCm", kind="scatter",ax=ax[0],label='setosa',color='r')
versicolor.plot(x="SepalLengthCm",y="SepalWidthCm",kind="scatter",ax=ax[0],label='versicolor',color='b')
virginica.plot(x="SepalLengthCm", y="SepalWidthCm", kind="scatter", ax=ax[0], label='virginica', color='g')

setosa.plot(x="PetalLengthCm", y="PetalWidthCm", kind="scatter",ax=ax[1],label='setosa',color='r')
versicolor.plot(x="PetalLengthCm",y="PetalWidthCm",kind="scatter",ax=ax[1],label='versicolor',color='b')
virginica.plot(x="PetalLengthCm", y="PetalWidthCm", kind="scatter", ax=ax[1], label='virginica', color='g')

ax[0].set(title='Sepal comparasion ', ylabel='sepal-width')
ax[1].set(title='Petal Comparasion',  ylabel='petal-width')
ax[0].legend()
ax[1].legend()

plt.show()
plt.close()
