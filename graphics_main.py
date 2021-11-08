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

    #plot trades
    for t in trades:
        fig1.plot([t[0], t[1]], [data[t[0]], data[t[1]]], label="Return {:.3f}".format(t[2]))

    plt.legend()
    plt.show()



loadData()
loadTrades()
createGraph()