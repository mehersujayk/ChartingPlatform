import pandas as pd
import requests
import yfinance as yf
import os
import iex



# with open('symbols.csv') as f:
#     lines = f.read().splitlines()
#     for symbol in lines:
#         data = yf.download(symbol, start='2021-05-24', end='2021-11-19')
#         data.to_csv('datasets/{}.csv'.format(symbol))

consolidatingTickers = iex.getConsolidatingTickers()

for ticker in consolidatingTickers:
    findDot = ticker.index('.')
    print(ticker[:findDot])



