#this file prints out the json trading files in a nicer form

import json

fileName = "trading.json"
tradingDictionary = {'closedTrades': [], 'openTrades': []}






def loadFile():
    global tradingDictionary

    f = open(fileName, "r")
    tradingDictionary = json.load(f)
    f.close()
    

def printResults():

    #variables
    runningTimeTotal = 0
    runningReturnTotal = 0
    returns = []

    loadFile()

    print("\nCompleted Trades")

    for t in tradingDictionary['closedTrades']:

        timeDifference = int(t['closeTime']) - int(t['openTime'])

        runningTimeTotal += timeDifference
        runningReturnTotal += float(t['percReturn'])
        returns.append(float(t['percReturn']))

        print("Buy Price: ${:.2f}\tSell Price: ${:.2f}\tTime Open: {:.2f}s\tReturn: {:.3f}%".format(float(t['openPrice']), float(t['closePrice']), timeDifference, float(t['percReturn'])))


    print("\nIncomplete Trades")

    for t in tradingDictionary['openTrades']:

        print("Buy Price: ${:.2f}\tSell Price: ${:.2f}\tReturn: {:.3f}%".format(float(t['openPrice']), float(t['closePrice']), float(t['percReturn'])))


    print("\n\nTrading Summary")
    print("Complete Trades {}".format(len(tradingDictionary['closedTrades'])))
    print("Incomplete Trades {}".format(len(tradingDictionary['openTrades'])))

    print("\nHighest Return {:.3f}%".format(max(returns)))
    print("Lowest Return {:.3f}%".format(min(returns)))

    print("\nAverage Return {:.3f}%".format(runningReturnTotal / len(tradingDictionary['closedTrades'])))
    print("Average Time {:.2f} Mins".format(runningTimeTotal / (len(tradingDictionary['closedTrades'] * 60))))




if __name__ == "__main__":
    printResults()