import requests
import pandas as pd
from collections import OrderedDict
from datetime import *
import os
from pandas import *
import numpy as np
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
IEX_API_TOKEN = 'pk_ac11dd54a2ec431ca0b113127eba593f' 


class stock(object):
    def __init__(self, stock):
        self.token = IEX_API_TOKEN
        self.baseURL = 'https://cloud.iexapis.com/stable'
        self.symbol = stock
    
    def getTickerSymbol(self):
        return self.symbol

    def getPrice(self):
        
        url = f'{self.baseURL}/stock/{self.symbol}/quote?token={self.token}'
        r = requests.get(url)
        data = [r.json()]
        #print(pd.json_normalize(data))

        return r.json()['iexClose']
    
    def getPrices(self, range, date):
        url = f'{self.baseURL}/stock/{self.symbol}/chart/{range}/{date}?token={self.token}'
        r = requests.get(url)
        return r.json()
    
    def getPricesIntradayMinutebar(self, range):
        url = f'{self.baseURL}/stock/{self.symbol}/chart/{range}?token={self.token}'
        r = requests.get(url)
        data = [r.json()]
        #print(pd.json_normalize(data))
        return r.json()
    
    def getPricesDailyOHLC(self, range):
        closePrices = OrderedDict()
        url = f'{self.baseURL}/stock/{self.symbol}/chart/{range}?token={self.token}'
        r = requests.get(url)
        data = r.json()
        #print(pd.json_normalize(data))

        for date in data:
            closePrices[date['date']] = [date['open'], date['high'], date['low'], date['close'], date['volume']]
        
        #print(closePrices)
        return closePrices

    
    
    def getName(self):
      url = f'{self.baseURL}/stock/{self.symbol}/company?token={self.token}'
      r = requests.get(url)
      data = r.json()

      return data['companyName']
    
    def getExchange(self):
      url = f'{self.baseURL}/stock/{self.symbol}/company?token={self.token}'
      r = requests.get(url)
      data = r.json()

      return data['exchange']
    

    def getHighestHighLowestLow(self, date):
        highs = []
        lows = []
        rummageThrough = self.getPricesDailyOHLC(date)

        for dat in rummageThrough:
            highs.append(rummageThrough[dat][1])
            lows.append(rummageThrough[dat][2])

        highestHigh = max(highs)
        lowestLow = min(lows)

        return (highestHigh, lowestLow)

    def getBeta(self):
        url = f'{self.baseURL}/stock/{self.symbol}/stats?token={self.token}'
        r = requests.get(url)
        beta = r.json()
        return beta['beta']

    def getStdDev(self, date):
        closeList = []
        closes = self.getPricesDailyOHLC(date)

        for close in closes:
            closeList.append(float(close[3]))

        mean = sum(closeList) / len(closeList)
        variance = sum([((x - mean) ** 2) for x in closeList]) / len(closeList)
        res = variance ** 0.5

        return res

    def getReturn(self, date):
        closes = self.getPricesDailyOHLC(date)

        finish = '2021-11-19'
        start = '2021-05-24'

        last = closes[finish][3]
        first = closes[start][0]

        totalReturn = (last - first) / first

        return totalReturn * 100
    
    def getRegressionValues(self):
        data = pd.DataFrame.from_dict(self.getPricesDailyOHLC('6m'), orient = 'index')
        return data


# I learned how AI prediction works using this video
# https://www.youtube.com/watch?v=hOLSGMEEwlI
# Naturally, some of the code is based off of the video, but it is heavily
# adapted to fit into my class and the ecosystem of functions I built for it
# to run off of
    def getAIValue(self, index):
        for filename in os.listdir('datasets'):
            symbol = filename.split('.')[0]
            

            df = pd.read_csv('datasets/{}'.format(filename))
            # if df.empty:
            #     return None
            
            if symbol.upper() == self.symbol.upper():
                df = df[['Close']]
                futureDays = 26

                #Create a new column (target)
                df['prediction'] = df[['Close']].shift(-futureDays)
                
                #Create the feature data set (X) and convert it to a numpy array and remove the last 'x' rows
                X = np.array(df.drop(['prediction'], 1))[:-futureDays]

                #Create the target set (Y) and convert to a numpy array and get all target values except for the last 'x' rows
                Y = np.array(df['prediction'])[:-futureDays]

                #Split data into training and testing
                x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.21875)

                #Create the tree regressor
                tree = DecisionTreeRegressor().fit(x_train, y_train)
                #Get the last x rows of the feature data set
                xFuture = df.drop(['prediction'], 1)[:-futureDays]

                #Get the last x rows of the feature data set
                xFuture = xFuture.tail(futureDays)

                xFuture = np.array(xFuture)
                treePred = tree.predict(xFuture)
                
                if index < len(treePred):
                    return treePred[index]

        return 1


            
    
    

       

       
        
   


    # def plot(ticker):
    #   data = ticker.getPricesDailyOHLC('20210415')
    #   #plotting on matplotlib mpl finance
    #   df = pd.DataFrame.from_dict(data, orient='index', columns=['Open', 'High', 'Low', 'Close', 'Volume'])

    #   df.index = pd.to_datetime(df.index)

    #   mc = mpf.make_marketcolors(up='b',down='r')
    #   s  = mpf.make_mpf_style(marketcolors=mc)
    #   mpf.plot(df['2021-01':'2021-10'],type = 'candle',title = ticker.getName(), volume = True, style='nightclouds')
        

def isConsolidating(df, percentage):
    recentCandlesticks = df[-15:]
    maxClose = recentCandlesticks['Close'].max()
    minClose = recentCandlesticks['Close'].min()

    threshhold = 1-(percentage/100)
    if minClose > (maxClose * threshhold):
        return True
    
    return False
    
def getConsolidatingTickers():
    consolidation = []
    for filename in os.listdir('datasets'):
        df = pd.read_csv('datasets/{}'.format(filename))
        if isConsolidating(df, 2.5):
            consolidation.append(filename)

    return consolidation    

def getTTMTickers():
    ttmTickers = []
    for filename in os.listdir('datasets'):
        symbol = filename.split('.')[0]
        
        df = pd.read_csv('datasets/{}'.format(filename))
        if df.empty:
            continue
        
        df['20sma'] = df['Close'].rolling(window=20).mean()
        df['stddev'] = df['Close'].rolling(window=20).std()
        df['upperband'] = df['20sma'] + (2 * df['stddev'])
        df['lowerband'] = df['20sma'] - (2 * df['stddev'])

        df['TR'] = abs(df['High'] - df['Low'])
        df['ATR'] = df['TR'].rolling(window = 10).mean()

        df['upperKC'] = df['20sma'] + (df['ATR'] * 1)
        df['lowerKC'] = df['20sma'] - (df['ATR'] * 1)

        #print(df)

        def inSqueeze(df):

            return df['upperband'] < df['upperKC'] and df['lowerband'] > df['lowerKC']
                
        df['squeeze on'] = df.apply(inSqueeze, axis=1)

        
        if df.iloc[-10]['squeeze on']:
            ttmTickers.append(symbol)
    
    return ttmTickers
        
        

        

