#this takes the trades file and the data file and plots the graphs

import matplotlib.pyplot as plt



#file names
dataFile = "dump12.txt"
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

    plt.legend()
    plt.show()



loadData()
loadTrades()
createGraph()