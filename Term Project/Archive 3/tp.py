'''
Name: Meher Sujay Kaky
AndrewID: mkaky
Hours Worked: 10
'''



from iex import stock
from cmu_112_graphics import *
from datetime import *

tickerSymbol = input()

ticker = stock(tickerSymbol)

stockHigh = int(ticker.getHighestHighLowestLow('20210415')[0])

stockLow = ticker.getHighestHighLowestLow('20210415')[1]



def appStarted(app):
    app.mode = 'homescreen'
    app.r = app.width/30
    app.graphWidth = 0 + app.width//10
    app.graphBottom = app.height - (app.height//10)
    app.graphTop = 0 + (app.height/10)
    app.graphHeight = app.graphTop - app.graphBottom
    app.increment = int(abs(app.graphHeight // 20))
    app.stockHigh = stockHigh
    app.stockLow = stockLow
    app.candleStickWidth = app.width // 200
    app.graphLeft = app.width//10
    app.graphRight = app.width - (app.width//10)


def homescreen_keyPressed(app, canvas):
    pass

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
    

def drawBase(app, canvas):
    stockFont = ("Comic Sans MS", 20, "bold")
    stockName = ticker.getName()
    w = app.width
    h = app.height
    canvas.create_line(0 + (w/10), 0 + (h/10), 0 + (w/10), h - (h/10), width=5)
    canvas.create_line(0 + (w/10), h-(h/10), w - (w/10), h - (h/10), width=5)
    canvas.create_text((w/2) - app.r, 0 + (h/20), text=stockName, font=stockFont)

def getTicks(app):
    #These are a bunch of variables used to calculate the pixel difference
    #per dollar of the stock
    graphDiff = app.graphBottom - app.graphTop
    stockDiff = app.stockHigh - app.stockLow
    pixelDiffPerDollarMove = graphDiff / stockDiff #change this if tkinter can't graph decimals
    OHLCValues = []
    prices = ticker.getPricesDailyOHLC('20210415')

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



def drawCandlesticks(app, canvas):
    OHLCValues = getTicks(app)

    
    w = app.width
    h = app.height

    date_format = "%m/%d/%Y"
    a = datetime.strptime('4/15/2021', date_format)
    b = datetime.strptime('11/18/2021', date_format)
    delta = b - a
    numDays = delta.days
    xaxisWidthInPixels = app.graphRight - app.graphLeft
    pixelsPerDay = xaxisWidthInPixels/numDays
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
    for day in range(numDays):
        

        if OHLCValues[day][3] >= OHLCValues[day][0]:

            canvas.create_rectangle((w//10) + (pixelsPerDay * day), 
                                    OHLCValues[day][3],
                                    (w//10) + (pixelsPerDay * day) + pixelsPerDay,
                                    OHLCValues[day][0], 
                                    fill = 'red')
            
            #top wick
            canvas.create_line((w//10) + (pixelsPerDay * (day)) + wickPixels,
                           OHLCValues[day][1], 
                           (w//10) + (pixelsPerDay * (day)) + wickPixels,
                           OHLCValues[day][0])

            #bottom wick
            canvas.create_line((w//10) + (pixelsPerDay * (day)) + wickPixels,
                           OHLCValues[day][3], 
                           (w//10) + (pixelsPerDay * (day)) + wickPixels,
                           OHLCValues[day][2])
        
        if OHLCValues[day][3] < OHLCValues[day][0]:
            canvas.create_rectangle((w//10) + (pixelsPerDay * day), 
                                    OHLCValues[day][3],
                                    (w//10) + (pixelsPerDay * day) + pixelsPerDay,
                                    OHLCValues[day][0], 
                                    fill = 'blue')
            
            #top wick
            canvas.create_line((w//10) + (pixelsPerDay * (day)) + wickPixels,
                           OHLCValues[day][1], 
                           (w//10) + (pixelsPerDay * (day)) + wickPixels,
                           OHLCValues[day][3])
            
            #bottom wick
            canvas.create_line((w//10) + (pixelsPerDay * (day)) + wickPixels,
                           OHLCValues[day][0], 
                           (w//10) + (pixelsPerDay * (day)) + wickPixels,
                           OHLCValues[day][2])

    

    

def drawDashes(app, canvas):
    diff = app.stockHigh - app.stockLow
    pixelsTopBottom = app.graphBottom - app.graphTop
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
    canvas.create_rectangle((w//2) + r, h/30, (w//2) + r + (r//2), h/30+(h/20), fill = 'red')
    canvas.create_text((w//2) + r + (r//4), h/30 + (h/60), text='Trade!')
    

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
    canvas.create_rectangle(w/16, (3*h)/20, w/2, h - (h/4), width=2)

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
    name = ticker.getName()
    canvas.create_text(w/2, h/10, text=f'Buy {name} stock', font=f'Arial {size} bold')

    #Number of shares
    canvas.create_text(w/6, h/3, text='Number of shares', font='Arial 18 bold')
    canvas.create_rectangle(w - (w/10) - (w/20), h/3 - (h/40),
                            w - (w/10) + (w/20), h/3 + (h/40))

def Buy_mousePressed(app, event):
    x = event.x
    y = event.y
    w = app.width
    h = app.height
    
    

    numSharesLeftX = w - (w/10) - (w/20)
    numSharesRightX = w - (w/10) + (w/20)
    numSharesTopY = h/3 - (h/40)
    numSharesBottomY = h/3 + (h/40)

    if x >= numSharesLeftX and x <= numSharesRightX and y >= numSharesTopY and y <= numSharesBottomY:
        app.numShares = app.getUserInput('how many shares would you like to buy?')
        
def Buy_drawShares(app, canvas):
    w = app.width
    h = app.height
    canvas.create_text(w - (w/10), h/3, text=f'{app.numShares}')
   
    

def Buy_redrawAll(app, canvas):
    Buy_drawBuyUI(app, canvas) 
    Buy_drawShares(app, canvas)   

runApp(width=800, height=800)


