import requests
import pandas as pd
import json


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
        #https://cloud.iexapis.com/stable/stock/xom/chart/20200415?token=pk_ac11dd54a2ec431ca0b113127eba593f
        closePrices = dict()
        url = f'{self.baseURL}/stock/{self.symbol}/chart/{date}?token={self.token}'
        r = requests.get(url)
        data = r.json()
        #print(pd.json_normalize(data))

        for date in data:
            closePrices[date['date']] = {date['open'], date['high'], date['low'], date['close']}
        
        print(closePrices)
        
        

        

