#import streamlit as st
import pandas as pd
import numpy
import requests
import module_manager
module_manager.review()
import plotly as plt
import config
from iex import stock

#st.title('Fundemental Dashboard')
token = config.IEX_API_TOKEN
tickerSymbol = input()

ticker = stock(tickerSymbol)


# baseURL = 'https://cloud.iexapis.com/stable'
# url = f'{baseURL}/stock/{tickerSymbol}/quote?token={stock.token}'
# instOwnership = f'{baseURL}/stock/aapl/institutional-ownership'
# r = requests.get(url)
# print(r.json()['iexClose'])

print(ticker.getPricesDailyOHLC('20200415'))




