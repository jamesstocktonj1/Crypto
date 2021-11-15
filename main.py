#main non-graphical trading from file

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


#trading dictionary
tradingDictionary = {}
tradingDictionary['openTrades'] = []
tradingDictionary['closedTrades'] = []




startTime = time.time()

#main file read loop
for l in f:

    l = l.strip()
    d = l.split(",")

    #add new data value
    trading.addValue(float(d[1]))
    trading.resizeBuffer()

    #perform calculations   
    trading.calculateValues()

    #execute trade (if required)
    trading.executeTrade()

    if(trading.newCurrentTrade()):

        tradingDictionary['openTrades'] += trading.getLatestOpenTrades()

        #write dictionary to json file
        jsonFile = open(exportFileName, "w")
        json.dump(tradingDictionary, jsonFile, indent=4, sort_keys=True)
        jsonFile.close()


    if(trading.newCompleteTrade()):

        completeTrades = trading.getLatestClosedTrades()

        tradingDictionary['closedTrades'] += completeTrades

        for t in tradingDictionary['openTrades']:
            
            for c in completeTrades:

                if(c['openTime'] == t['openTime']):
                    tradingDictionary['openTrades'].remove(t)

        #write dictionary to json file
        jsonFile = open(exportFileName, "w")
        json.dump(tradingDictionary, jsonFile, indent=4, sort_keys=True)
        jsonFile.close()

endTime = time.time()

f.close()

print("Last Point: {}".format(trading.totalPosition))



totalReturn = 0
complexReturn = 1
returnList = []


print("\nCompleted Trades")
for t in tradingDictionary['closedTrades']:

    print("Closed Trade: Buy {:.4f}\tSell {:.4f}\tReturn {:.3f}%".format(t['openPrice'], t['closePrice'], t['percReturn']))

    totalReturn += float(t['percReturn'])
    returnList.append(float(t['percReturn']))

    #using 10x leverage
    complexReturn *= ((float(t['percReturn'] / 100) * 10) + 1)


print("\nIncomplete Trades")
for t in tradingDictionary['openTrades']:

    print("Open Trade: Buy {:.4f}\tReturn {:.3f}%".format(t['openPrice'], t['percReturn']))


print("\n\nSummary\nClosed Trades: {}".format(len(tradingDictionary['closedTrades'])))
print("Open Trades: {}".format(len(tradingDictionary['openTrades'])))

#min/max
print("\nHighest Return: {:.3f}%".format(max(returnList)))
print("Lowest Return: {:.3f}%".format(min(returnList)))

#returns
print("\nTotal Return: {:.4f}%".format(totalReturn))
print("Compound Return: {:.4f}%".format(complexReturn))
print("Average Return: {:.3f}%".format(totalReturn / len(tradingDictionary['closedTrades'])))

#time performance analysis
print("\n{} data points analysed in {:.2f}s".format(trading.totalPosition, (endTime - startTime)))


#write dictionary to json file
jsonFile = open(exportFileName, "w")
json.dump(tradingDictionary, jsonFile, indent=4, sort_keys=True)
jsonFile.close()



plt.grid()
plt.show()