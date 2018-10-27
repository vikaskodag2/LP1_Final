iris
nrow(iris)
ncol(iris)
str(iris)  #https://www.statmethods.net/input/contents.html to display types of variables
typeof(iris$Sepal.Length)
typeof(iris$Sepal.Width)
typeof(iris$Petal.Length)
typeof(iris$Petal.Width)
typeof(iris$Species)

#prinitng summary of all features
summary(iris)
min(iris$Sepal.Length)
max(iris$Sepal.Length)
mean(iris$Sepal.Length)
median(iris$Sepal.Length)
range(iris$Sepal.Length)
sd(iris$Sepal.Length)
var(iris$Sepal.Length)
summary(iris$Sepal.Length)

#ploting histogram
hist(iris$Sepal.Length)
hist(iris$Sepal.Width)
hist(iris$Petal.Length)
hist(iris$Petal.Width)

#ploting boxplots
boxplot(iris,horizontal = TRUE) #horizontal boxplots
boxplot(iris) #https://www.r-bloggers.com/use-box-plots-to-assess-the-distribution-and-to-identify-the-outliers-in-your-dataset/noc
boxplot(iris$Sepal.Width,notch = TRUE) #plot boxplot with notch

#finding outliers in boxplot 
boxplot.stats(iris$Sepal.Width)$out  #refer https://stat.ethz.ch/R-manual/R-devel/library/grDevices/html/boxplot.stats.html
