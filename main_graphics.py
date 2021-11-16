#main graphical trading from file

from src.Algorithm import *
from src.SimpleAlgorithm import *
import matplotlib.pyplot as plt
import time
import json


#import file
importFileName = "continuousdata.txt"
exportFileName = "trading.json"

f = open(importFileName, "r")


#initialise trading object
trading = SimpleAlgorithm()


#list of current trades
completeTrades = []
incompleteTrades = []

data = []

startTime = time.time()

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


endTime = time.time()

f.close()

#get remaining open trades
incompleteTrades = trading.getCurrentTrades()

fig1 = plt.subplot(1, 1, 1)

fig1.plot(range(0, len(data)), data)
fig1.plot(range(0, len(trading.MA25)), trading.MA25)
fig1.plot(range(0, len(trading.runningRunningAverage)), trading.runningRunningAverage)

print("Last Point: {}".format(trading.totalPosition))



totalReturn = 0
complexReturn = 1
returnList = []


print("\nCompleted Trades")
for t in completeTrades:

    print("Closed Trade: Buy {:.4f}\tSell {:.4f}\tReturn {:.3f}%".format(t['openPrice'], t['closePrice'], t['percReturn']))

    fig1.plot([t['openTime'], t['closeTime']], [t['openPrice'], t['closePrice']])

    totalReturn += float(t['percReturn'])
    returnList.append(float(t['percReturn']))

    #using 10x leverage
    complexReturn *= ((float(t['percReturn'] / 100) * 10) + 1)


print("\nIncomplete Trades")
for t in incompleteTrades:

    print("Open Trade: Buy {:.4f}\tReturn {:.3f}%".format(t['openPrice'], t['percReturn']))


print("\n\nSummary\nClosed Trades: {}".format(len(completeTrades)))
print("Open Trades: {}".format(len(incompleteTrades)))

#min/max
print("\nHighest Return: {:.3f}%".format(max(returnList)))
print("Lowest Return: {:.3f}%".format(min(returnList)))

#returns
print("\nTotal Return: {:.4f}%".format(totalReturn))
print("Compound Return: {:.4f}%".format(complexReturn))
print("Average Return: {:.3f}%".format(totalReturn / len(completeTrades)))

#time performance analysis
print("\n{} data points analysed in {:.2f}s".format(len(data), (endTime - startTime)))

#create dictionary of all trades
tradingDictionary = {}
tradingDictionary['closedTrades'] = completeTrades
tradingDictionary['openTrades'] = incompleteTrades

#write dictionary to json file
jsonFile = open(exportFileName, "w")
json.dump(tradingDictionary, jsonFile, indent=4, sort_keys=True)
jsonFile.close()



plt.grid()
plt.show()