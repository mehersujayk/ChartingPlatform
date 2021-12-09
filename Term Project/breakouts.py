import os
import pandas as pd

def isConsolidating(df, percentage):
    recentCandlesticks = df[:100]
    maxClose = recentCandlesticks['Close'].max()
    minClose = recentCandlesticks['Close'].min()

    threshhold = 1-(percentage/100)
    if minClose > (maxClose * threshhold):
        return True
    
    return False

def isBreakingOut(df, percentage):
    threshhold = 1 - (percentage/100)
    if not df.size < 20:
        lastClose = df[-1:]['Close'].values[0]
        if isConsolidating(df[-16:-1], threshhold):
            recentCloses = df[-16:-1]

            if lastClose > recentCloses['Close'].max():
                return True
    
    return False



for filename in os.listdir('datasets'):
    df = pd.read_csv('datasets/{}'.format(filename))
    if isConsolidating(df, 10):
        print(filename)
    
    
