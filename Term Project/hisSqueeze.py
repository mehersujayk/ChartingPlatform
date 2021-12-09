import iex
import os
import numpy as np
import pandas as pd
from iex import stock
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import matplotlib.pyplot as plt  # To visualize
from sklearn.preprocessing import MinMaxScaler
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split


# print("Hello World!")


# name = 'AAPL'

# s = stock(name)
# data = pd.DataFrame.from_dict(s.getPricesDailyOHLC('6m'), orient = 'index')


# df = data[[3]]
# futureDays = 26
# print(df.shape)

# df['Prediction'] = df[[3]].shift(-futureDays)

# df = df.reshape(-1, 1)

# data_train = np.array(df[:int(df.shape[0]*0.8)])




# dataList = data.values.tolist()
# hundredDataList = dataList[:100]
# #print(hundredDataList)
# dataClone = pd.DataFrame(hundredDataList)
# #print(dataClone)
# hundredData = data[:100]




# X = dataClone.iloc[:, 0].values.reshape(-1, 1)  # values converts it into a numpy array
# Y = dataClone.iloc[:, 3].values.reshape(-1, 1)  # -1 means that calculate the dimension of rows, but have 1 column
# linear_regressor = LinearRegression()  # create object for the class
# linear_regressor.fit(X, Y)  # perform linear regression
# Y_pred = linear_regressor.predict(X)  # make predictions
# #print(Y_pred)

# poly = PolynomialFeatures(degree = 4)
# X_poly = poly.fit_transform(X)
 
# poly.fit(X_poly, Y)
# lin2 = LinearRegression()
# lin2.fit(X_poly, Y)
# YPolyPred = lin2.predict(poly.fit_transform(X))

#print(YPolyPred)


# plt.scatter(X, Y)
# plt.plot(X, YPolyPred, color='red')
# plt.show()

name = 'AMZN'


for filename in os.listdir('datasets'):
    symbol = filename.split('.')[0]

    df = pd.read_csv('datasets/{}'.format(filename))
    if df.empty:
        continue

    if symbol == name:

        df = df[['Close']]
        futureDays = 26

        #Create a new column (target)
        df['prediction'] = df[['Close']].shift(-futureDays)
        print(df)
        

        #Create the feature data set (X) and convert it to a numpy array and remove the last 'x' rows
        X = np.array(df.drop(['prediction'], 1))[:-futureDays]
        
        print(X.shape)
        #Create the target set (Y) and convert to a numpy array and get all target values except for the last 'x' rows
        Y = np.array(df['prediction'])[:-futureDays]
        print(Y.shape)
        #Split the data into training and testing
        #x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.20)
        x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.21875)

        #Create the tree regressor model
        tree = DecisionTreeRegressor().fit(x_train, y_train)

        #Get the last x rows of the feature data set
        xFuture = df.drop(['prediction'], 1)[:-futureDays]

        #Get the last x rows of the feature data set
        xFuture = xFuture.tail(futureDays)

        xFuture = np.array(xFuture)
        treePred = tree.predict(xFuture)
        
        print(treePred[0])


