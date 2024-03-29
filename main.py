#main non-graphical trading from file

from src.Algorithm import *
from src.SimpleAlgorithm import *
from src.TrendingAlgorithm import *
from binance.client import Client
import time
import json


#import file
#importFileName = "continuousdata.txt"
#exportFileName = "trading.json"
#importFileName = "dump12_2.txt"
exportFileName = "trading12_2.json"

appendTrades = True


f = open("cred.txt", "r")

api_key = str(f.readline().strip())
api_secret = str(f.readline().strip())

f.close()

print(api_key)
print(api_secret)


client = Client(api_key, api_secret)
client.API_URL = 'https://api.binance.com/api'


#initialise trading object
trading = TrendingAlgorithm()


#trading dictionary
tradingDictionary = {}
tradingDictionary['openTrades'] = []
tradingDictionary['closedTrades'] = []

if(appendTrades):
    jsonFile = open(exportFileName, "r")
    tradingDictionary = json.load(jsonFile)
    jsonFile.close()

else:
    jsonFile = open(exportFileName, "w")
    json.dump(tradingDictionary, jsonFile, indent=4, sort_keys=True)
    jsonFile.close()


#main trading loop
while True:

    startTime = time.time()

    eth_price = client.get_margin_price_index(symbol="ETHUSDT")

    #add new data value
    trading.addValue(float(eth_price['price']))
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

    if((trading.totalPosition % 60) == 0):
        print("Time: {}:{:02d}".format(int(trading.totalPosition / 3600), int(((trading.totalPosition / 3600) % 60) * 60)))

    while(time.time() < (startTime + 1)):
        pass






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