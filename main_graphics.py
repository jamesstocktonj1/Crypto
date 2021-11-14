#main graphical trading from file

from src.Algorithm import *
from src.SimpleAlgorithm import *
import matplotlib.pyplot as plt


#import file
importFileName = "continuousdata.txt"

f = open(importFileName, "r")


#initialise trading object
trading = SimpleAlgorithm()


#list of current trades
completeTrades = []
incompleteTrades = []

data = []



#main file read loop
for l in f:

    l = l.strip()
    d = l.split(",")
    data.append(float(d[1]))

    #add new data value
    trading.addValue(float(d[1]))
    trading.resizeBuffer()

    #perform calculations   
    trading.calculateValues()

    #execute trade (if required)
    trading.executeTrade()


    if(trading.newCompleteTrade()):
        completeTrades += trading.getLatestClosedTrades()

    
#get remaining open trades
incompleteTrades = trading.getCurrentTrades()

fig1 = plt.subplot(1, 1, 1)

fig1.plot(range(0, len(data)), data)




totalReturn = 0
returnList = []


print("Completed Trades")
for t in completeTrades:

    print("Closed Trade: Buy {:.4f}\tSell {:.4f}\tReturn {:.3f}%".format(t['openPrice'], t['closePrice'], t['percReturn']))

    fig1.plot([t['openTime'], t['closeTime']], [t['openPrice'], t['closePrice']])

    totalReturn += float(t['percReturn'])
    returnList.append(float(t['percReturn']))


print("Incomplete Trades")
for t in incompleteTrades:

    print("Open Trade: Buy {:.4f}\tReturn {:.3f}%".format(t['openPrice'], t['percReturn']))


print("\n\nSummary\nClosed Trades: {}".format(len(completeTrades)))
print("Open Trades: {}".format(len(incompleteTrades)))

print("\nHighest Return: {:.3f}%".format(max(returnList)))
print("Lowest Return: {:.3f}%".format(min(returnList)))

print("\nTotal Return: {:.4f}%".format(totalReturn))
print("Average Return: {:.3f}%".format(totalReturn / len(completeTrades)))

plt.show()