import os, pandas as pd


# i = 0
# ttmTickers = []
# for filename in os.listdir('datasets'):
#     #print(filename)
#     symbols = ['AAPL']
#     symbol = filename.split('.')[0]
    
#     df = pd.read_csv('datasets/{}'.format(filename))
#     if df.empty:
#         continue
    
#     df['20sma'] = df['Close'].rolling(window=20).mean()
#     df['stddev'] = df['Close'].rolling(window=20).std()
#     df['upperband'] = df['20sma'] + (2 * df['stddev'])
#     df['lowerband'] = df['20sma'] - (2 * df['stddev'])

#     df['TR'] = abs(df['High'] - df['Low'])
#     df['ATR'] = df['TR'].rolling(window = 10).mean()

#     df['upperKC'] = df['20sma'] + (df['ATR'] * 1)
#     df['lowerKC'] = df['20sma'] - (df['ATR'] * 1)

#     #print(df)

#     def inSqueeze(df):

#         return df['upperband'] < df['upperKC'] and df['lowerband'] > df['lowerKC']
            
#     df['squeeze on'] = df.apply(inSqueeze, axis=1)

    
#     if df.iloc[-10]['squeeze on']:
#         i += 1
#         ttmTickers.append(symbol)



# print(ttmTickers)


def getTTMTickers():
    ttmTickers = []
    for filename in os.listdir('datasets'):
        
        symbol = filename.split('.')[0]
        
        df = pd.read_csv('datasets/{}'.format(filename))
        if symbol == 'AAPL':
            print(filename)
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
        
        
        
print(getTTMTickers())