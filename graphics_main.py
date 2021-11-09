#this takes the trades file and the data file and plots the graphs

import matplotlib.pyplot as plt
from liveAnalysis import *



#file names
dataFile = "dump12_2.txt"
tradeFile = "trad.txt"

data = []
trades = []


def loadData():
    
    f = open(dataFile, "r")

    for l in f:
        l = l.strip()
        d = l.split(",")
        data.append(float(d[1]))

    f.close()


def loadTrades():

    f = open(tradeFile, "r")

    for l in f:
        l = l.strip()
        d = l.split(",")
        trades.append([int(d[0]), int(d[1]), float(d[2])])

    f.close()


def addAdditionalLines(fig):

    MA25 = []
    MA99 = []

    for d in data:
        curPos = data.index(d)

        if(curPos > 26):
            MA25.append(runningIntegral(data[(curPos - 25):(curPos + 1)], 25))
        else:
            MA25.append(None)
        
        if(curPos > 100):
            MA99.append(runningIntegral(data[(curPos - 99):(curPos + 1)], 99))
        else:
            MA99.append(None)

    fig.plot(range(0, len(MA25)), MA25, label="MA25")
    fig.plot(range(0, len(MA99)), MA99, label="MA99")




def createGraph():

    #create subplot
    fig1 = plt.subplot(1, 1, 1)

    #plot ETH data
    fig1.plot(range(0, len(data)), data)


    justReturns = []

    buyVal = []
    sellVal = []
    returnVal = []

    sortedReturn = []

    for t in trades:
        buyVal.append(t[0])
        sellVal.append(t[1])
        returnVal.append(t[2])

        sortedReturn.append(t[2])

    sortedReturn.sort(reverse=True)
    

    #plot trades
    for t in sortedReturn:
        
        n = returnVal.index(t)

        #only mark legend with the first (x) highest returns
        if(n < 5):
            fig1.plot([buyVal[n], sellVal[n]], [data[buyVal[n]], data[sellVal[n]]], label="Return {:.3f}".format(t))
        else:
            fig1.plot([buyVal[n], sellVal[n]], [data[buyVal[n]], data[sellVal[n]]])

    #addAdditionalLines(fig1)


    plt.legend()
    plt.show()



loadData()
loadTrades()
createGraph()