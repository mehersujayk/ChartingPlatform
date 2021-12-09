import numpy as np
import pandas as pd
import pandas_datareader as pdr
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sb
sb.set()
import os
from sklearn.linear_model import LinearRegression



finish = '2021-11-19'
start = '2021-05-24'
spy = pdr.get_data_yahoo('SPY', start = start, end=finish)
spydf = spy['Close']
spyReturns = (np.log(spydf).diff()).dropna()
print(spyReturns)

for filename in os.listdir('datasets'):
    symbol = filename.split('.')[0]
    df = pd.read_csv('datasets/{}'.format(filename))
    data = df['Close']
    returns = (np.log(data).diff()).dropna()
    if symbol == 'AAPL':
        idx = df[0].first_valid_index()
        print(idx)
        df.index.get_loc(idx)
        print(returns)    
        print(returns.corr(spyReturns))
