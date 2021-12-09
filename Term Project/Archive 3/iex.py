import requests
import pandas as pd


IEX_API_TOKEN = 'pk_ac11dd54a2ec431ca0b113127eba593f' 


class stock(object):
    def __init__(self, stock):
        self.token = IEX_API_TOKEN
        self.baseURL = 'https://cloud.iexapis.com/stable'
        self.symbol = stock
    
    def getPrice(self):
        
        url = f'{self.baseURL}/stock/{self.symbol}/quote?token={self.token}'
        r = requests.get(url)
        data = [r.json()]
        print(pd.json_normalize(data))

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
    
    def getPricesDailyOHLC(self, date):
        closePrices = dict()
        url = f'{self.baseURL}/stock/{self.symbol}/chart/{date}?token={self.token}'
        r = requests.get(url)
        data = r.json()
        #print(pd.json_normalize(data))

        for date in data:
            closePrices[date['date']] = [date['open'], date['high'], date['low'], date['close'], date['volume']]
        
        print(closePrices)
        return closePrices
    
    def getName(self):
      url = f'{self.baseURL}/stock/{self.symbol}/company?token={self.token}'
      r = requests.get(url)
      data = r.json()

      return data['companyName']
    

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
        
       
        



    # def plot(ticker):
    #   data = ticker.getPricesDailyOHLC('20210415')
    #   #plotting on matplotlib mpl finance
    #   df = pd.DataFrame.from_dict(data, orient='index', columns=['Open', 'High', 'Low', 'Close', 'Volume'])

    #   df.index = pd.to_datetime(df.index)

    #   mc = mpf.make_marketcolors(up='b',down='r')
    #   s  = mpf.make_mpf_style(marketcolors=mc)
    #   mpf.plot(df['2021-01':'2021-10'],type = 'candle',title = ticker.getName(), volume = True, style='nightclouds')
        
        

        

