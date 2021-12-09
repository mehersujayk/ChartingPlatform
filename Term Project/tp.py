'''
Name: Meher Sujay Kaky
AndrewID: mkaky
Hours Worked: 30
'''
from iex import stock
import iex
from cmu_112_graphics import *
from datetime import *
from dateutil.relativedelta import relativedelta
import math
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import pandas as pd


def appStarted(app):
    
    #general setup
    app.stock = 'aapl'
    tickerSymbol = app.stock
    app.ticker = stock(tickerSymbol)
    app.prices = app.ticker.getPricesDailyOHLC('6m')
    highestHighLowestLow = app.ticker.getHighestHighLowestLow('6m')
    stockHigh = int(highestHighLowestLow[0])
    stockLow = highestHighLowestLow[1]
    app.mode = 'loadScreen'
    app.r = app.width/30
    app.graphWidth = 0 + app.width//10
    app.graphBottom = app.height - (app.height//10)
    app.graphTop = 0 + (app.height/10)
    app.graphHeight = app.graphTop - app.graphBottom
    app.stockHigh = stockHigh

    app.stockLow = stockLow

    #chart setup
    
    app.increment = int(abs(app.graphHeight // 20))
    app.candleStickWidth = app.width // 200
    app.graphLeft = app.width//10
    app.graphRight = app.width - (app.width//10)
    
    app.numShares = 0
    app.numSharesToSell = 0
    
    #app.stockprice = app.prices[99][3]
    app.months = 6
    app.holidays = 5
    app.b = datetime.today() - relativedelta(days=1)
    app.a = app.b - relativedelta(months=app.months)

    app.priceItems = app.prices.items()
    app.priceItemsList = list(app.priceItems)
    
    app.firstHundred = list(app.priceItems)[:100]
    app.firstHundredDict = dict(app.firstHundred)
    
    app.day = 100
    app.stockprice = app.firstHundred[-1][1][3]
    app.isMoveRight = False
    app.isMoveLeft = False
    app.moveRight = 5
    app.moveLeft = 5
    app.numTimesMovedRight = 0
    app.numTimesMovedLeft = 0

    app.data = app.ticker.getRegressionValues()
    app.dataList = app.data.values.tolist()
    app.hundredDataList = app.dataList[:100]
    app.dataClone = pd.DataFrame(app.hundredDataList)
    print(app.dataClone)
    app.dataClone['20sma'] = app.dataClone[3].rolling(window=20).mean()
    app.dataClone['9sma'] = app.dataClone[3].rolling(window=9).mean()
    
    
    app.AIValue = app.ticker.getAIValue(app.day - 100)
    
    if app.AIValue != None and app.AIValue >= app.firstHundred[-1][1][3]:
        app.AIBuySell = True
    else:
        app.AIBuySell = False

    app.stockMessage = ''
    app.newStockTriggered = False
    app.newStockDone = False
    app.zoomTriggered = False
    #Order setup
    app.limitBuyPrice = app.stockprice
    app.limitSellPrice = app.stockprice
    app.exchange = app.ticker.getExchange()
    app.buyTotal = app.limitBuyPrice * app.numShares
    app.sellTotal = app.limitSellPrice * app.numShares
    app.buys = dict()
    app.money = 100000
    
    #Portfolio Stuff
    app.isbuy = False

    #Analytics Stuff
    app.betas = []
    app.devs = []

def drawLoadScreenUI(app, canvas):
    w = app.width
    h = app.height
    r = h/8
    #welcome message
    canvas.create_text(w/2, h/10, text = 'Tradingview Lite: Trading Reimagined', font='Arial 20 bold')

    #options

    #Charts
    canvas.create_rectangle(w/2 - r, h/3, w/2 + r, h/3 + (h/10), fill = 'dark turquoise')
    canvas.create_text(w/2, h/3 + (h/20), text = 'Charts', font='Arial 14 bold')

    #portfolio
    canvas.create_rectangle(w/2 - r, h/2, w/2 + r, h/2 + (h/10), fill = 'SpringGreen3')
    canvas.create_text(w/2, (2*h)/4 + (h/20), text = 'Portfolio', font='Arial 14 bold')

    
def loadScreen_mousePressed(app, event):
    w = app.width
    h = app.height
    r = h/8
    x = event.x
    y = event.y
    #if charts is pressed
    chartsLeftX = w/2 - r
    chartsRightX = w/2 + r
    chartsBottomY = h/3 + (h/10)
    chartsTopY = h/3

    if x >= chartsLeftX and x <= chartsRightX and y >= chartsTopY and y <= chartsBottomY:
        app.mode = 'homescreen'

    #if portfolio is pressed
    portLeftX = w/2 - r
    portRightX = w/2 + r
    portBottomY = h/2 + (h/10)
    portTopY = h/2

    if x >= portLeftX and x <= portRightX and y >= portTopY and y <= portBottomY:
        app.mode = 'mainPort'
    pass

def loadScreen_redrawAll(app, canvas):
    drawLoadScreenUI(app, canvas)
    pass


##### Homescreen stuff




def homescreen_keyPressed(app, event):
    key = event.key
    print('pressed', key)

    if key == '3':
        app.stockMessage = ''


    if app.newStockTriggered:

        if key in 'abcdefghijklmnopqrstuvwxyz':
            app.stockMessage += key
        if len(app.stockMessage) > 5:
            app.newStockTriggered = False
            app.newStockDone = True
    

    if key == 'Enter':
        print(app.stockMessage)
        app.newStockDone = True
        app.newStockTriggered = False
    

    if key == '/':
        print('pressed', key)
        s = app.getUserInput('Please input a new stock symbol!')
        
        app.ticker = stock(s)
        
        highestHighLowestLow = app.ticker.getHighestHighLowestLow('6m')
        
        stockHigh = int(highestHighLowestLow[0])
        
        stockLow = highestHighLowestLow[1]
        
        app.stockHigh = stockHigh
        
        app.stockLow = stockLow
        
        app.prices = app.ticker.getPricesDailyOHLC('6m')
        
    
    if key == 'Up':
        print('pressed!')
        newDate = '3m'
        highestHighLowestLow = app.ticker.getHighestHighLowestLow(newDate)
        stockHigh = int(highestHighLowestLow[0])
        stockLow = highestHighLowestLow[1]
        app.stockHigh = stockHigh
        app.stockLow = stockLow
        app.prices = app.ticker.getPricesDailyOHLC(newDate)
        app.months = 3
        app.a = app.b - relativedelta(months=app.months)
        app.holidays = 3

    if key == 'Down':
        print('pressed!')
        newDate = '6m'
        highestHighLowestLow = app.ticker.getHighestHighLowestLow(newDate)
        stockHigh = int(highestHighLowestLow[0])
        stockLow = highestHighLowestLow[1]
        app.stockHigh = stockHigh
        app.stockLow = stockLow
        app.prices = app.ticker.getPricesDailyOHLC(newDate)
        app.months = 6
        app.a = app.b - relativedelta(months=app.months)
        app.holidays = 5




def homescreen_mousePressed(app, event):
    w = app.width
    h = app.height
    r = w//4
    x = event.x
    y = event.y



    leftXBound = (w//2) + r
    rightXBound = (w//2) + r + (r//2)
    bottomYBound = h/30+(h/20)
    upperYBound = h/30

    if x >= leftXBound and x < rightXBound and y < bottomYBound and y >= upperYBound:
        app.mode = 'mainPort'

    newStockLeftX = app.graphLeft
    newStockRightX = app.graphLeft + (w/8)
    newStockTopY = h - (h/15)
    newStockBottomY = h - (h/30)

    

    if x >= newStockLeftX and x <= newStockRightX and y <= newStockBottomY and y >= newStockTopY:
        print('pressed')
        app.newStockTriggered = True
        if app.newStockDone:
            print('NewStockTriggered!')
            s = app.stockMessage
            if s == None or len(s) > 5:
                app.showMessage('This is not a stock! Please input the ticker symbol for your stock!')
            else: 
                app.ticker = stock(s)
                highestHighLowestLow = app.ticker.getHighestHighLowestLow('6m')
                stockHigh = int(highestHighLowestLow[0])
                stockLow = highestHighLowestLow[1]
                app.stockHigh = stockHigh
                app.stockLow = stockLow
                app.prices = app.ticker.getPricesDailyOHLC('6m')
                app.priceItems = app.prices.items()
                app.priceItemsList = list(app.priceItems)
                app.data = app.ticker.getRegressionValues()
                app.dataList = app.data.values.tolist()


                if app.day < len(app.priceItems) and app.day < len(app.dataList):
                    app.firstHundred = list(app.priceItems)[(app.day - 100):app.day]
                    app.hundredDataList = app.dataList[(app.day-100):app.day]
                else:
                    app.firstHundred = list(app.priceItems)[0:100]
                    app.hundredDataList = app.dataList[0:100]
                
                app.dataClone = pd.DataFrame(app.hundredDataList)
                app.dataClone['20sma'] = app.dataClone[3].rolling(window=20).mean()
                app.dataClone['9sma'] = app.dataClone[3].rolling(window=9).mean()
                app.firstHundredDict = dict(app.firstHundred)
                app.stockprice = app.firstHundred[-1][1][3]
                app.limitBuyPrice = app.stockprice
                app.limitSellPrice = app.stockprice
                app.buyTotal = 0.0
                app.AIValue = app.ticker.getAIValue(app.day-100)
                if app.AIValue != None and app.AIValue >= app.firstHundred[-1][1][3]:
                    app.AIBuySell = True
                else:
                    app.AIBuySell = False  
    app.newStockDone = False
        
        

    zoomInLeftX = w/2 - (w/16)
    zoomInRightX = w/2 + (w/16)
    zoomInBottomY = h - (h/15)
    zoomInTopY = h - (h/30)

    
    if x >= zoomInLeftX and x <= zoomInRightX and y >= zoomInBottomY and y <= zoomInTopY:
        app.zoomTriggered = True
        newDate = '3m'
        highestHighLowestLow = app.ticker.getHighestHighLowestLow(newDate)
        stockHigh = int(highestHighLowestLow[0])
        stockLow = highestHighLowestLow[1]
        app.stockHigh = stockHigh
        app.stockLow = stockLow
        app.prices = app.ticker.getPricesDailyOHLC(newDate)
        
        app.priceItems = app.prices.items()
        app.priceItemsList = list(app.priceItems)
        
        app.firstHundred = list(app.priceItems)[:50]
        app.hundredDataList = app.dataList[:50]
        
        app.firstHundredDict = dict(app.firstHundred)
        
        app.months = 3
        app.a = app.b - relativedelta(months=app.months)
        app.holidays = 3


    zoomOutLeftX = app.graphRight - (w/8)
    zoomOutRightX = app.graphRight
    zoomOutBottomY = h - (h/15)
    zoomOutTopY = h - (h/30)

    if x >= zoomOutLeftX and x <= zoomOutRightX and y >= zoomOutBottomY and y <= zoomOutTopY:
        app.zoomTriggered = False
        newDate = '6m'
        highestHighLowestLow = app.ticker.getHighestHighLowestLow(newDate)
        stockHigh = int(highestHighLowestLow[0])
        stockLow = highestHighLowestLow[1]
        app.stockHigh = stockHigh
        app.stockLow = stockLow
        app.prices = app.ticker.getPricesDailyOHLC(newDate)
        app.prices = app.ticker.getPricesDailyOHLC(newDate)
        
        app.priceItems = app.prices.items()
        app.priceItemsList = list(app.priceItems)
        
        app.firstHundred = list(app.priceItems)[(app.day - 100):app.day]
        app.firstHundredDict = dict(app.firstHundred)
        app.months = 6
        app.a = app.b - relativedelta(months=app.months)
        app.holidays = 5

    #press move right
    rightMoveLeftX = app.graphRight - (w/4)
    rightMoveRightX = app.graphRight - (w/4) + (w/64)
    rightMoveBottomY = h - (h/30)
    rightMoveTopY = h - (h/15)

    if x >= rightMoveLeftX and x <= rightMoveRightX and y <= rightMoveBottomY and y >= rightMoveTopY:
        if app.day < len(app.priceItemsList):
            toAdd = app.priceItemsList[app.day]
            toAddRegression = app.dataList[app.day]
            app.firstHundred.pop(0)
            app.hundredDataList.pop(0)
            app.firstHundred.append(toAdd)  
            app.hundredDataList.append(toAddRegression)
            app.dataClone = pd.DataFrame(app.hundredDataList)
            app.dataClone['20sma'] = app.dataClone[3].rolling(window=20).mean()
            app.dataClone['9sma'] = app.dataClone[3].rolling(window=9).mean()
            app.firstHundredDict = dict(app.firstHundred)
            app.stockprice = app.firstHundred[-1][1][3]
            app.limitBuyPrice = app.stockprice
            app.limitSellPrice = app.stockprice
            app.buyTotal = 0.0
            app.day += 1
            app.AIValue = app.ticker.getAIValue(app.day - 100)
            if app.AIValue != None and app.AIValue >= app.firstHundred[-1][1][3]:
                app.AIBuySell = True
            else:
                app.AIBuySell = False   
        else:
            app.showMessage('That is the end of the dataset! Thanks for playing!')


        
    
    
    #press move left
    leftMoveLeftX = app.graphLeft + (w/4)
    leftMoveRightX = app.graphLeft + (w/4) + (w/64)
    leftMoveBottomY = h - (h/30)
    leftMoveTopY = h - (h/15)

    if x >= leftMoveLeftX and x <= leftMoveRightX and y <= leftMoveBottomY and y >= leftMoveTopY:
        daysSince = app.day - 100
        if daysSince > 0:
            toAdd = app.priceItemsList[daysSince]
            app.firstHundred.pop()
            app.firstHundred.insert(0, toAdd)
            app.firstHundredDict = dict(app.firstHundred)
            app.stockprice = app.firstHundred[-1][1][3]
            app.limitBuyPrice = app.stockprice
            app.limitSellPrice = app.stockprice
            app.buyTotal = 0.0
            app.day -= 1
            app.AIValue = app.ticker.getAIValue(app.day - 100)
            if app.AIValue != None and app.AIValue >= app.firstHundred[-1][1][3]:
                app.AIBuySell = True
            else:
                app.AIBuySell = False
        else:
            app.showMessage('No more historical data to show!')


def drawBase(app, canvas):
    stockFont = ("Comic Sans MS", 20, "bold")
    stockName = app.ticker.getName()
    w = app.width
    h = app.height
    canvas.create_line(0 + (w/10), 0 + (h/10), 0 + (w/10), h - (h/10), width=5)
    canvas.create_line(0 + (w/10), h-(h/10), w - (w/10), h - (h/10), width=5)
    canvas.create_text((w/2) - app.r, 0 + (h/20), text=stockName, font=stockFont)

def getTicks(app, arr):
    #These are a bunch of variables used to calculate the pixel difference
    #per dollar of the stock
    graphDiff = app.graphBottom - app.graphTop
    stockDiff = app.stockHigh - app.stockLow
    pixelDiffPerDollarMove = graphDiff / stockDiff #change this if tkinter can't graph decimals
    OHLCValues = []
    prices = arr

    #calculates the pixel difference for open, high, low, and close
    #and adds them to a list
    for date in prices:
        dollarDiff = prices[date][0] - prices[date][3]
        pixelDiff = pixelDiffPerDollarMove * dollarDiff
        open = app.graphBottom - (prices[date][0] - app.stockLow) * pixelDiffPerDollarMove
        high = app.graphBottom - (prices[date][1] - app.stockLow) * pixelDiffPerDollarMove
        low = app.graphBottom - (prices[date][2] - app.stockLow) * pixelDiffPerDollarMove
        close = app.graphBottom - (prices[date][3] - app.stockLow) * pixelDiffPerDollarMove
        priceLst = [open, high, low, close]
        
            
        OHLCValues.append(priceLst)

    
    
    #return the OHLC values
    return OHLCValues

#I got this function directly from stackoverflow page that was dedicated
#to helping me find the number of weekdays between two given dates
#https://stackoverflow.com/questions/3615375/number-of-days-between-2-dates-excluding-weekends
 
def get_workdays(from_date: datetime, to_date: datetime):
    # if the start date is on a weekend, forward the date to next Monday
    if from_date.weekday() > 4:
        from_date = from_date + timedelta(days=7 - from_date.weekday())
    # if the end date is on a weekend, rewind the date to the previous Friday
    if to_date.weekday() > 4:
        to_date = to_date - timedelta(days=to_date.weekday() - 4)
    if from_date > to_date:
        return 0
    # that makes the difference easy, no remainders etc
    diff_days = (to_date - from_date).days + 1
    weeks = int(diff_days / 7)
    return weeks * 5 + (to_date.weekday() - from_date.weekday()) + 1




def drawCandlesticks(app, canvas):
    graphDiff = app.graphBottom - app.graphTop
    stockDiff = app.stockHigh - app.stockLow
    pixelDiffPerDollarMove = graphDiff / stockDiff
    OHLCValues = getTicks(app, app.prices)
    
    #This code is adapted from https://www.geeksforgeeks.org/python-implementation-of-polynomial-regression/
    X = app.dataClone.iloc[:, 1].values.reshape(-1, 1)  # values converts it into a numpy array
    Y = app.dataClone.iloc[:, 2].values.reshape(-1, 1)  # -1 means that calculate the dimension of rows, but have 1 column
    poly = PolynomialFeatures(degree = 4)
    X_poly = poly.fit_transform(X)
    
    poly.fit(X_poly, Y)
    lin2 = LinearRegression()
    lin2.fit(X_poly, Y)
    YPolyPred = lin2.predict(poly.fit_transform(X))
    
    
    w = app.width
    firstHundred = getTicks(app, app.firstHundredDict)
    
    numDays = get_workdays(app.a, app.b) - app.holidays
    #print(numDays)
    xaxisWidthInPixels = app.graphRight - app.graphLeft
    pixelsPerDay = xaxisWidthInPixels/len(app.firstHundred)
    wickPixels = pixelsPerDay / 2
    
    #drawing a candlestick

    #top wick
    
    
    #body
    #using the Open and Close values from OHLC Values, I created the bodies
    #at the correct places in the chart and moved the candlesticks the perfect
    #amount by calculating the pixels per day in the x direction and adding it
    #to the x coordinate

    #wicks
    #using the high, low, close, and open values, I constructed wicks for the
    #stock that represent how high and how low the price reached before it 
    #it settled at its close price


    for day in range(len(firstHundred)):
        if firstHundred[day][3] >= firstHundred[day][0]:

            canvas.create_rectangle((w//10) + (pixelsPerDay * day), 
                                    firstHundred[day][3],
                                    (w//10) + (pixelsPerDay * day) + pixelsPerDay,
                                    firstHundred[day][0], 
                                    fill = 'red')
            
            #top wick
            canvas.create_line((w//10) + (pixelsPerDay * (day)) + wickPixels,
                           firstHundred[day][1], 
                           (w//10) + (pixelsPerDay * (day)) + wickPixels,
                           firstHundred[day][0])

            #bottom wick
            canvas.create_line((w//10) + (pixelsPerDay * (day)) + wickPixels,
                           firstHundred[day][3], 
                           (w//10) + (pixelsPerDay * (day)) + wickPixels,
                           firstHundred[day][2])
        
        if firstHundred[day][3] < firstHundred[day][0]:
            canvas.create_rectangle((w//10) + (pixelsPerDay * day), 
                                    firstHundred[day][3],
                                    (w//10) + (pixelsPerDay * day) + pixelsPerDay,
                                    firstHundred[day][0], 
                                    fill = 'blue')
            
            #top wick
            canvas.create_line((w//10) + (pixelsPerDay * (day)) + wickPixels,
                           firstHundred[day][1], 
                           (w//10) + (pixelsPerDay * (day)) + wickPixels,
                           firstHundred[day][3])
            
            #bottom wick
            canvas.create_line((w//10) + (pixelsPerDay * (day)) + wickPixels,
                           firstHundred[day][0], 
                           (w//10) + (pixelsPerDay * (day)) + wickPixels,
                           firstHundred[day][2])

    if not app.zoomTriggered:

        for value in range(len(YPolyPred) - 1):
            firstValue = app.graphBottom - (YPolyPred[value] - app.stockLow) * pixelDiffPerDollarMove
            lastValue = app.graphBottom - (YPolyPred[value+1] - app.stockLow) * pixelDiffPerDollarMove
            canvas.create_line(app.graphLeft + (pixelsPerDay * value), int(firstValue), app.graphLeft + (pixelsPerDay* (value + 1)), int(lastValue), fill = 'black', width=2)

        for val in range(app.dataClone.shape[0] - 1):
            value = app.dataClone['20sma'][val]
            nextValue = app.dataClone['20sma'][val+1]
            
            if math.isnan(value) or math.isnan(nextValue):
                continue
            
            plotVal = app.graphBottom - (value - app.stockLow) * pixelDiffPerDollarMove
            plotNextVal = app.graphBottom - (nextValue - app.stockLow) * pixelDiffPerDollarMove
            canvas.create_line(app.graphLeft + (pixelsPerDay * val), int(plotVal), app.graphLeft + (pixelsPerDay * (val + 1)), int(plotNextVal), fill = 'green', width=2)

        for sma in range(app.dataClone.shape[0] - 1):
            value = app.dataClone['9sma'][sma]
            nextValue = app.dataClone['9sma'][sma+1]

        

            if math.isnan(value) or math.isnan(nextValue):
                continue

            plotVal = app.graphBottom - (value-app.stockLow) * pixelDiffPerDollarMove
            plotNextVal = app.graphBottom - (nextValue-app.stockLow) * pixelDiffPerDollarMove
            
            canvas.create_line(app.graphLeft + (pixelsPerDay * sma), int(plotVal), app.graphLeft + (pixelsPerDay * (sma + 1)), int(plotNextVal), fill='MediumOrchid2', width=2)

    


def drawDashes(app, canvas):
    diff = app.stockHigh - app.stockLow
    increment = diff / 21
    
    

    for x in range(1,21):
        height = app.graphBottom - (x * app.increment) + (app.height//80)
        price = (app.stockLow + (x * increment))
        

        canvas.create_text(app.graphWidth-(app.width/25),
                           height, text='{:0.2f}'.format(price) )
        
def drawDates(app, canvas):
    date_format = "%m/%d/%Y"
    a = datetime.strptime('4/15/2021', date_format)
    b = datetime.strptime('11/17/2021', date_format)
    delta = b - a
    numDays = delta.days
    xaxisWidthInPixels = app.graphRight - app.graphLeft
    pixelsPerDay = xaxisWidthInPixels/numDays
    daysToNextPrint = numDays // 3
    pixelsToNextPrint = daysToNextPrint * pixelsPerDay

def drawUI(app, canvas):
    w = app.width
    h = app.height
    r = w//4
    
    #Trade button
    canvas.create_rectangle((w//2) + r, h/30, (w//2) + r + (r//2), h/30+(h/20), fill = 'red')
    canvas.create_text((w//2) + r + (r//4), h/30 + (h/60), text='Trade!')
    
    #New stock button
    canvas.create_rectangle(app.graphLeft, h - (h/15), app.graphLeft + (w/8), h - (h/30), fill='cyan')
    canvas.create_text(app.graphLeft + (w/16), h - (h/20), text = app.stockMessage)

    #zoom in button
    canvas.create_rectangle(w/2 - (w/16), h - (h/15), w/2 + (w/16), h - (h/30), fill='lavender blush')
    canvas.create_text(w/2, h - (h/20), text = 'zoom in!')
    
    #zoom out button
    canvas.create_rectangle(app.graphRight - (w/8), h - (h/15), app.graphRight, h - (h/30), fill='lavender blush')
    canvas.create_text(app.graphRight - (w/16), h - (h/20), text = 'zoom out!')

    #move right
    canvas.create_rectangle(app.graphRight - (w/4), h - (h/15), app.graphRight - (w/4) + (w/64),  h - (h/30), fill = 'green')

    #move left
    canvas.create_rectangle(app.graphLeft + (w/4), h - (h/15), app.graphLeft + (w/4) + (w/64), h - (h/30), fill = 'red')



def homescreen_redrawAll(app, canvas):
    drawBase(app, canvas)
    drawDashes(app, canvas)
    drawCandlesticks(app, canvas)
    drawUI(app, canvas)
    


##### Main Port Screen Stuff

def mainPort_mousePressed(app, event):
    w = app.width
    h = app.height
    x = event.x
    y = event.y
    #if the analytics button is pressed
    analLeftX = w - (w/4)
    analRightX = w - (w/8)
    analTopY = h/20
    analBottomY = h/10

    if x >= analLeftX and x <= analRightX and y >= analTopY and y <= analBottomY:
        app.mode = 'Analytics'
    
    #if the buy button is pressed
    buyLeftX = w/16
    buyRightX = w/4
    buyTopY = h - (h/6)
    buyBottomY = h - (h/12)

    if x >= buyLeftX and x <= buyRightX and y >= buyTopY and y <= buyBottomY:
        app.mode = 'Buy'
    
    #if the sell button is pressed
    sellLeftX = w/2 - ((3*w) / 32)
    sellRightX = w/2 + ((3*w) / 32)
    sellTopY = h - (h/6)
    sellBottomY = h - (h/12)

    if x >= sellLeftX and x <= sellRightX and y >= sellTopY and y <= sellBottomY:
        app.mode = 'Sell'
    
    #if the screener button is pressed
    screenerLeftX = w - (w/4)
    screenerRightX = w - (w/16)
    screenerTopY = h - (h/6)
    screenerBottomY = h - (h/12)

    if x >= screenerLeftX and x <= screenerRightX and y >= screenerTopY and y <= screenerBottomY:
        app.mode = 'Screener'
    
    #if the back button is pressed
    backLeftX = w/2 + (w/30)
    backRightX = w/2 + (w/30) + (w/8)
    backBottomY = h/10
    backTopY = h/20

    if x >= backLeftX and x <= backRightX and y >= backTopY and y <= backBottomY:
        app.mode = 'homescreen'
    

def drawMainPortUI(app, canvas):
    w = app.width
    h = app.height
    r = w//10


    #Create Portfolio sign
    canvas.create_text(w/4, h/20 + (h/40), text='Portfolio', font=f'Arial {r} bold')

    #Create Analytics Sign 
    canvas.create_rectangle(w - (w/4), h/20, w - (w/8), h/10, fill='CadetBlue2')
    canvas.create_text(w - (3*w)/16, (3*w)/40, text='Analytics')

    #Create Stock Box
    #canvas.create_rectangle(w/16, (3*h)/20, w/2, h - (h/4), width=2)
    if len(app.buys) > 0:
        stockIncrement = ((12*h) / 20) / 5
    i = 0
    for stocky in app.buys:

        if int(app.buys[stocky][0]) > 0 and len(app.buys) == 1:
            canvas.create_text(w/8, (h*3)/15, text=stocky, anchor='w', font='Arial 20')
            canvas.create_text(w/2, (h*3)/15, text=app.buys[stocky][0], font = 'Arial 20')
        elif int(app.buys[stocky][0]) > 0:
            canvas.create_text(w/8, (h*3)/15 + (stockIncrement * i), text=stocky, anchor='w', font='Arial 20')
            canvas.create_text(w/2, (h*3)/15 + (stockIncrement * i), text=app.buys[stocky][0], font = 'Arial 20')

        i += 1


    #create buy sign
    canvas.create_rectangle(w/16, h - (h/6), w/4, h - (h/12), fill='SeaGreen1')
    canvas.create_text(w/8 + (w/32), h - ((3 * h) / 24), text = 'Buy!')

    #create sell sign
    canvas.create_rectangle(w/2 - ((3*w) / 32), h - (h/6), w/2 + ((3*w) / 32), h - (h/12), fill='IndianRed1')
    canvas.create_text(w/2, h - ((3 * h) / 24), text = 'Sell!')

    #create screener sign
    canvas.create_rectangle(w - (w/4), h - (h/6), w - (w/16), h - (h/12), fill='orchid1')
    canvas.create_text(w - (w/8 + (w/32)), h - ((3 * h) / 24), text='Screeners')

    #create back sign
    canvas.create_rectangle(w/2 + (w/30), h/20, 
                            w/2 + (w/30) + (w/8), h/10, 
                            fill = 'bisque')

    canvas.create_text(w/2 + (w/30) + (w/16), h/20 + (h/40),
                       text = 'Back!')

    pass


def mainPort_redrawAll(app, canvas):
    drawMainPortUI(app, canvas)
    pass


##### Buy Screen Stuff

def Buy_drawBuyUI(app, canvas):
    w = app.width
    h = app.height

    #Draw label
    size = w//20
    name = app.ticker.getName()
    canvas.create_text(w/2, h/10, text=f'Buy {name} stock', font=f'Arial {size} bold')

    #current Share price
    canvas.create_text(w/2, h/5,
                       text=f'Current Price: {app.stockprice}',
                       font=f'Arial 20 bold')

    #back button
    canvas.create_rectangle(w/30, h/40, w/30 + (w/8), h/20, fill = 'bisque')
    canvas.create_text(w/30 + (w/16), h/40 + (h/80), text='Back!')

    #Amount of money left
    canvas.create_text(w/2, (2.5*h)/10, text=f'Money Left: {app.money}', font='Arial 24 bold', anchor='center')

    #Number of shares
    canvas.create_text(w/6, (4*h)/10, text='Number of shares', font='Arial 18 bold')
    canvas.create_rectangle(w - (w/10) - (w/20), (4*h)/10 - (h/40),
                            w - (w/10) + (w/20), (4*h)/10 + (h/40))
    canvas.create_text(w - (w/10), (4*h)/10, text=f'{app.numShares}')

    #limit price
    canvas.create_text(w/8, (2*h)/4, text='Limit Price', font='Arial 18 bold')
    canvas.create_rectangle(w - (w/10) - (w/20), (2*h)/4 - (h/40),
                            w - (w/10) + (w/20), (2*h)/4 + (h/40))
    canvas.create_text(w - (w/10), (2*h)/4, text=f'{app.limitBuyPrice}')

    #AI Buy or Sell
    canvas.create_text(w/12, (5*h)/8, text='AI Buy Sell', font='Arial 18 bold', anchor='w')
    if app.AIBuySell:
        canvas.create_text(w - (w/10), (5*h)/8, text='AI Buy', anchor='e')
    else:
        canvas.create_text(w - (w/10), (5*h)/8, text='AI Sell', anchor='e')

    #buy total
    canvas.create_text(w/10, h - (h/4), text = 'Total', font='Arial 18 bold')
    canvas.create_text(w - (w/10), h - (h/4), text=f'{app.buyTotal}')

    #buy button
    canvas.create_rectangle(w/2 - ((3*w) / 32), h - (h/6), w/2 + ((3*w) / 32), h - (h/12), fill='SeaGreen1')
    canvas.create_text(w/2, h - ((3 * h) / 24), text = 'Buy!')
    

def Buy_mousePressed(app, event):
    x = event.x
    y = event.y
    w = app.width
    h = app.height
    stockname = app.ticker.getName()
    

    numSharesLeftX = w - (w/10) - (w/20)
    numSharesRightX = w - (w/10) + (w/20)
    numSharesTopY = (4*h)/10 - (h/40)
    numSharesBottomY = (4*h)/10 + (h/40)
   
    if x >= numSharesLeftX and x <= numSharesRightX and y >= numSharesTopY and y <= numSharesBottomY:
        app.numShares = app.getUserInput('how many shares would you like to buy?')
        if app.numShares == None or int(app.numShares) < 0:
            app.showMessage('Please enter a valid number for the num shares or go back!')
            app.numShares = 0
        else:
            app.buyTotal = int(app.numShares) * float(app.limitBuyPrice)
    
    limitPriceLeftX = w - (w/10) - (w/20)
    limitPriceRightX = w - (w/10) + (w/20)
    limitPriceTopY = (2*h)/4 - (h/40)
    limitPriceBottomY = (2*h)/4 + (h/40)
        
    if x >= limitPriceLeftX and x <= limitPriceRightX and y >= limitPriceTopY and y <= limitPriceBottomY:
        limitPrice = app.getUserInput('What price would you like to buy at?')
        if limitPrice == None:
            app.showMessage('Please enter a valid number for the limit price or go back!')
            limitPrice = 0
        else:
            if float(limitPrice) < math.floor(app.stockprice) or float(limitPrice) > math.ceil(app.stockprice):
                app.showMessage('Excessive price deviation, please keep your prices to within a dollar')
            else:
                app.limitPrice = limitPrice
                app.buyTotal = int(app.numShares) * float(app.limitBuyPrice)

    backLeftX = w/30
    backRightX = w/30 + (w/8)
    backBottomY = h/20
    backTopY = h/40

    if x >= backLeftX and x <= backRightX and y >= backTopY and y <= backBottomY:
        app.mode = 'mainPort'

    #When the buy button is pressed
    buyButtonLeftX = w/2 - ((3*w) / 32)
    buyButtonRightX = w/2 + ((3*w) / 32)
    buyButtonBottomY = h - (h/12)
    buyButtonTopY = h - (h/6)

    if x >= buyButtonLeftX and x <= buyButtonRightX and y >= buyButtonTopY and y <= buyButtonBottomY:
        if len(app.buys) + 1 > 5:
            app.showMessage('5 stocks is the max! Please sell one position to add another!')
        else:
            app.isbuy = True
            if stockname in app.buys:
                app.buys[stockname][0] += int(app.numShares)
            else:
                app.buys[stockname] = [int(app.numShares), app.stockprice]
                app.buys[stockname].append(app.ticker.getBeta())
                app.buys[stockname].append(app.ticker.getStdDev('6m'))
                app.buys[stockname].append(app.priceItemsList)
                app.money -= app.buyTotal
                app.numShares = 0 
                app.buyTotal = 0
    
    

def Buy_redrawAll(app, canvas):
    Buy_drawBuyUI(app, canvas) 



#### Sell Screen Stuff

def Sell_drawBuyUI(app, canvas):
    w = app.width
    h = app.height

    #Draw label
    size = w//20
    name = app.ticker.getName()
    canvas.create_text(w/2, h/10, text=f'Buy {name} stock', font=f'Arial {size} bold')

    #current Share price
    canvas.create_text(w/2, h/5,
                       text=f'Current Price: {app.stockprice}',
                       font=f'Arial {size//2} bold')

    #back button
    canvas.create_rectangle(w/30, h/40, w/30 + (w/8), h/20, fill = 'bisque')
    canvas.create_text(w/30 + (w/16), h/40 + (h/80), text='Back!')

    #Number of shares
    canvas.create_text(w/6, h/3, text='Number of shares', font='Arial 18 bold')
    canvas.create_rectangle(w - (w/10) - (w/20), h/3 - (h/40),
                            w - (w/10) + (w/20), h/3 + (h/40))
    canvas.create_text(w - (w/10), h/3, text=f'{app.numSharesToSell}')

    #limit price
    canvas.create_text(w/8, (2*h)/4, text='Limit Price', font='Arial 18 bold')
    canvas.create_rectangle(w - (w/10) - (w/20), (2*h)/4 - (h/40),
                            w - (w/10) + (w/20), (2*h)/4 + (h/40))
    canvas.create_text(w - (w/10), (2*h)/4, text=f'{app.limitSellPrice}')

    #AI Buy or Sell
    canvas.create_text(w/12, (5*h)/8, text='AI Buy Sell', font='Arial 18 bold', anchor='w')
    if app.AIBuySell:
        canvas.create_text(w - (w/10), (5*h)/8, text='AI Buy', anchor='e')
    else:
        canvas.create_text(w - (w/10), (5*h)/8, text='AI Sell', anchor='e')

    #sell total
    canvas.create_text(w/10, h - (h/4), text = 'Total', font='Arial 18 bold')
    canvas.create_text(w - (w/10), h - (h/4), text=f'{app.sellTotal}')

    #sell button
    canvas.create_rectangle(w/2 - ((3*w) / 32), h - (h/6), w/2 + ((3*w) / 32), h - (h/12), fill='IndianRed1')
    canvas.create_text(w/2, h - ((3 * h) / 24), text = 'Sell!')
    

def Sell_mousePressed(app, event):
    x = event.x
    y = event.y
    w = app.width
    h = app.height
    stockname = app.ticker.getName()
    

    numSharesLeftX = w - (w/10) - (w/20)
    numSharesRightX = w - (w/10) + (w/20)
    numSharesTopY = h/3 - (h/40)
    numSharesBottomY = h/3 + (h/40)

    if x >= numSharesLeftX and x <= numSharesRightX and y >= numSharesTopY and y <= numSharesBottomY:
        app.numSharesToSell = app.getUserInput('how many shares would you like to sell?')
        if app.numSharesToSell == None or int(app.numSharesToSell) < 0:
            app.showMessage('Please enter a valid number of shares or go back!')
            app.numSharesToSell = 0
        else:
            app.sellTotal = int(app.numSharesToSell) * float(app.limitSellPrice)
    
    limitPriceLeftX = w - (w/10) - (w/20)
    limitPriceRightX = w - (w/10) + (w/20)
    limitPriceTopY = (2*h)/4 - (h/40)
    limitPriceBottomY = (2*h)/4 + (h/40)
        
    if x >= limitPriceLeftX and x <= limitPriceRightX and y >= limitPriceTopY and y <= limitPriceBottomY:
        limitPrice = app.getUserInput('What price would you like to sell at?')
        if limitPrice == None:
            app.showMessage('Please enter a valid limit price or go back!')
            limitPrice = 0
        else:
            if float(limitPrice) < math.floor(app.stockprice) or float(limitPrice) > math.ceil(app.stockprice):
                app.showMessage('Excessive price deviation, please keep your prices to within a dollar')
            else:
                app.limitSellPrice = limitPrice
                app.sellTotal = int(app.numSharesToSell) * float(app.limitSellPrice)
        
    backLeftX = w/30
    backRightX = w/30 + (w/8)
    backBottomY = h/20
    backTopY = h/40

    if x >= backLeftX and x <= backRightX and y >= backTopY and y <= backBottomY:
        app.mode = 'mainPort'
   
    
    #When the buy button is pressed
    sellButtonLeftX = w/2 - ((3*w) / 32)
    sellButtonRightX = w/2 + ((3*w) / 32)
    sellButtonBottomY = h - (h/12)
    sellButtonTopY = h - (h/6)

    if x >= sellButtonLeftX and x <= sellButtonRightX and y >= sellButtonTopY and y <= sellButtonBottomY:
        print('sell pressed!')
        if stockname in app.buys:
            app.buys[stockname][0] -= int(app.numSharesToSell)
            if app.buys[stockname][0] <= 0:
                app.buys.pop(stockname)
            app.money += app.sellTotal
            
        else:
            app.showMessage('That stock does not exist in your portfolio!')
        
        app.numSharesToSell = 0
        app.sellTotal = 0
   
    

def Sell_redrawAll(app, canvas):
    Sell_drawBuyUI(app, canvas) 





#### Analytics stuff



def drawAnalyticsUI(app, canvas):
    w = app.width
    h = app.height
    r = w//10
    stockname = app.ticker.getName()

    #Draw Label
    canvas.create_text(w/4, h/20 + (h/40), text='Analytics', font=f'Arial {r} bold')

    #back button
    canvas.create_rectangle(w/2 + (w/30), h/20, 
                            w/2 + (w/30) + (w/8), h/10, 
                            fill = 'bisque')
    
    canvas.create_text(w/2 + (w/30) + (w/16), h/20 + (h/40),
                       text = 'Back!')

    #Display Beta
    canvas.create_text(w/10, h/3, text='Beta', font='Arial 18 bold', anchor='w')
    totalBeta = 0
    if len(app.buys) != 0:
        for thing in app.buys:
            totalBeta += app.buys[thing][2]
        beta = totalBeta / len(app.buys)
    else:
        beta = totalBeta

    canvas.create_text(w - (w/10), h/3, text='{:0.2f}'.format(beta))

    #Display Standard Deviation
    stdDev = 0
    totalStdDev = 0
    if len(app.buys) != 0:
        for buy in app.buys:
            totalStdDev += app.buys[buy][3]
        stdDev = totalStdDev / len(app.buys)
    
    canvas.create_text(w/10, (2*h)/5, text='Std Dev', font = 'Arial 18 bold', anchor='w')
    canvas.create_text(w - (w/10), (2*h)/5, text='{:0.2f}'.format(stdDev))


    #Display total return
    totalReturn = 0
    actualReturn = 0
    
    
    for buy in app.buys:
        currentPrice = app.buys[buy][4][app.day][1][3]
        print(currentPrice)
        boughtPrice = app.buys[buy][1]
        print(boughtPrice)
        print()
        returnOfStock = (currentPrice - boughtPrice) / boughtPrice
        totalReturn += returnOfStock

    if totalReturn != 0:
        actualReturn = (totalReturn / len(app.buys)) * 100
    else:
        actualReturn = 0
    
    canvas.create_text(w/10, (7*h)/15, text='Return', font = 'Arial 18 bold', anchor='w')
    canvas.create_text(w - (w/10), (7*h)/15, text='{:0.2f}%'.format(actualReturn))

    #display treynor
    riskFreeRate = 1.54
    treynor = 0
    if beta != 0:
        treynor = (actualReturn - riskFreeRate) / beta
    canvas.create_text(w/10, (8*h)/15, text='Treynor Measure', font = 'Arial 18 bold', anchor='w')
    canvas.create_text(w - (w/10), (8*h)/15, text='{:0.2f}%'.format(treynor))

    #display jenson's alpha
    marketRiskFreeRate = 10
    capm = riskFreeRate + beta*(marketRiskFreeRate)
    jenson = actualReturn - capm

    canvas.create_text(w/10, (9*h)/15, text='Jenson\'s Alpha', font = 'Arial 18 bold', anchor='w')
    canvas.create_text(w - (w/10), (9*h)/15, text='{:0.2f}%'.format(jenson))

    #Display Sharpe Ratio





def Analytics_mousePressed(app, event):
    x = event.x
    y = event.y
    w = app.width
    h = app.height
    

    #if the back button is pressed
    backLeftX = w/2 + (w/30)
    backRightX = w/2 + (w/30) + (w/8)
    backBottomY = h/10
    backTopY = h/20

    if x >= backLeftX and x <= backRightX and y >= backTopY and y <= backBottomY:
        app.mode = 'mainPort'

def Analytics_redrawAll(app, canvas):
    drawAnalyticsUI(app, canvas)
    pass



####### Screener stuff

def drawScreenerUI(app, canvas):
    w = app.width
    h = app.height
    r = w//10
    #back button
    canvas.create_rectangle(w/2 + (w/30), h/20, 
                            w/2 + (w/30) + (w/8), h/10, 
                            fill = 'bisque')
    
    canvas.create_text(w/2 + (w/30) + (w/16), h/20 + (h/40),
                       text = 'Back!')
    
    #Draw Label
    canvas.create_text(w/4, h/20 + (h/40), text='Screeners', font=f'Arial {r} bold')

    #Draw label for consolidation screener
    canvas.create_text(w/7, h/6, text='Consolidation Stocks', font='Arial 13 bold')

    #draw consolidation stocks
    i = 0
    consolidatingTickers = iex.getConsolidatingTickers()
    increment = ((h - (h/15)) - (h/6 + (h/40))) / len(consolidatingTickers)
    for ticker in consolidatingTickers:
        findDot = ticker.index('.')
        toPrint = ticker[:findDot]
        canvas.create_text(w/8, h/6 + (h/40) + (increment * i), text=toPrint)
        i+=1

    #TTM Squeeze Label
    canvas.create_text(w - (w/7), h/6, text='TTM Squeeze Stocks', font='Arial 13 bold')

    i = 0
    ttmTickers = iex.getTTMTickers()

    for tick in ttmTickers:
        canvas.create_text(w - (w/8), h/6 + (h/40) + (increment * i), text=tick)
        i+=1
    


def Screener_mousePressed(app, event):
    x = event.x
    y = event.y
    w = app.width
    h = app.height

    #if the back button is pressed
    backLeftX = w/2 + (w/30)
    backRightX = w/2 + (w/30) + (w/8)
    backBottomY = h/10
    backTopY = h/20

    if x >= backLeftX and x <= backRightX and y >= backTopY and y <= backBottomY:
        app.mode = 'mainPort'



def Screener_redrawAll(app, canvas):
    w = app.width
    h = app.height


    drawScreenerUI(app, canvas)


runApp(width=800, height=800)


