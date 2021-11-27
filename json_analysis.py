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

    compoundReturn = 1
    compoundXReturn = 1
    compoundYReturn = 1

    loadFile()

    print("\nCompleted Trades")

    for t in tradingDictionary['closedTrades']:

        timeDifference = int(t['closeTime']) - int(t['openTime'])

        runningTimeTotal += timeDifference
        runningReturnTotal += float(t['percReturn'])
        returns.append(float(t['percReturn']))

        compoundReturn *= 1 + (float(t['percReturn']) * 0.01)
        compoundXReturn *= 1 + (float(t['percReturn']) * 0.01 * 10 * 0.05)
        compoundYReturn *= 1 + (float(t['percReturn']) * 0.01 * 25 * 0.05)

        print("Buy Price: ${:.2f}\tSell Price: ${:.2f}\tTime Open: {}:{:02d}\tReturn: {:.3f}%".format(float(t['openPrice']), float(t['closePrice']), int(timeDifference / 60), int(((timeDifference / 60) % 1) * 60), float(t['percReturn'])))


    print("\nIncomplete Trades")

    for t in tradingDictionary['openTrades']:

        print("Buy Price: ${:.2f}\tSell Price: ${:.2f}\tReturn: {:.3f}%".format(float(t['openPrice']), float(t['closePrice']), float(t['percReturn'])))


    print("\n\nTrading Summary")
    print("Complete Trades {}".format(len(tradingDictionary['closedTrades'])))
    print("Incomplete Trades {}".format(len(tradingDictionary['openTrades'])))

    print("\nHighest Return {:.3f}%".format(max(returns)))
    print("Lowest Return {:.3f}%".format(min(returns)))

    compoundReturn = (compoundReturn - 1) * 100
    compoundXReturn = (compoundXReturn - 1) * 100
    compoundYReturn = (compoundYReturn - 1) * 100

    print("\nCompound Return {:.3f}%".format(compoundReturn))
    print("Compound 10x Return {:.3f}%".format(compoundXReturn))
    print("Compound 25x Return {:.3f}%".format(compoundYReturn))

    averageTime = runningTimeTotal / (len(tradingDictionary['closedTrades'] * 60))

    print("\nAverage Return {:.3f}%".format(runningReturnTotal / len(tradingDictionary['closedTrades'])))
    print("Average Time {}:{:02d}".format(int(averageTime), int((averageTime % 1) * 60)))




if __name__ == "__main__":
    printResults()