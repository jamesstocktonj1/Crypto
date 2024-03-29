#main graphical trading from file

from src.Algorithm import *
from src.SimpleAlgorithm import *
from src.TrendingAlgorithm import *
from src.FIRAlgorithm import *
import matplotlib.pyplot as plt
import time
import json
import math


#import file
#importFileName = "ethData1.txt"
#exportFileName = "ethData1.json"
importFileName = "continuousdata3.txt"
exportFileName = "trading.json"
#importFileName = "dump12_2.txt"
#exportFileName = "trading12_2.json"

f = open(importFileName, "r")


#initialise trading object
#trading = SimpleAlgorithm()
trading = TrendingAlgorithm()
#trading = FIRAlgorithm()


#list of current trades
completeTrades = []
incompleteTrades = []

data = []



#main file read loop
for l in f:

    l = l.strip()
    d = l.split(",")
    data.append(float(d[1]))

f.close()


bankAccount = 1000
rollingBank = []

startTime = time.time()

for d in data:
    #add new data value
    trading.addValue(float(d))
    trading.resizeBuffer()

    #perform calculations   
    trading.calculateValues()

    #execute trade (if required)
    trading.executeTrade()

    if(trading.newCompleteTrade()):
        completeTrades += trading.getLatestClosedTrades()

        for t in trading.getLatestClosedTrades():

            bankAccount += (rollingBank[t['openTime']] * 0.05 * t['percReturn']  * 0.01 * 10)
            print("Money Made: £{:.4f}".format((rollingBank[t['openTime']] * 0.05 * t['percReturn']  * 0.01 * 10)))


    if((trading.totalPosition % 1000) == 0):
        print("Position: {}".format(trading.totalPosition))
    
    rollingBank.append(bankAccount)

endTime = time.time()

#get remaining open trades
incompleteTrades = trading.getCurrentTrades()

fig1 = plt.subplot(1, 1, 1)
#fig2 = plt.subplot(2, 1, 2)

fig1.plot(range(0, len(data)), data)
#fig1.plot(range(len(data) - len(trading.MA25), len(data)), trading.MA25)
#fig1.plot(range(0, len(trading.filterValues)), trading.filterValues)

#fig2.plot(range(0, len(trading.runningAverageD)), trading.runningAverageD)
#fig2.plot(range(0, len(trading.MA25D)), trading.MA25D)
#fig2.plot(range(0, len(trading.filterValuesD)), trading.filterValuesD)




upperBound = []
lowerBound = []
for p in trading.runningRunningAverage:
    upperBound.append(p * 1.02)
    lowerBound.append(p * 0.98)

fig1.plot(range(0, len(trading.runningRunningAverage)), trading.runningRunningAverage)
fig1.plot(range(0, len(upperBound)), upperBound)
fig1.plot(range(0, len(lowerBound)), lowerBound)




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
    complexReturn *= (((float(t['percReturn'] / 100) * 10) * 0.05) + 1)

try:
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

    #money analysis
    print("\nMoney Analysis\nBank Account: ${:.2f}".format(bankAccount))
    hourlyReturn = math.exp(math.log(bankAccount / rollingBank[0]) / (len(data) / 3600)) - 1
    print("Hourly Return: {:.4f}%".format(hourlyReturn * 100))
    doublingFactor = math.log(2) / math.log(hourlyReturn + 1)
    print("Doubling Factor: {:.1f} hours".format(doublingFactor))

    #time performance analysis
    print("\n{} data points analysed in {:.2f}s".format(len(data), (endTime - startTime)))
except:
    pass

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