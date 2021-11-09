#main non-graphical stock analysis and practice buying program


from liveAnalysis import *
from algorithm import *





#file import
fileName = "dump12.txt"
filePoint = 0
fileData = []
dataAvailable = True

#load data to fileData
f = open(fileName, "r")
for line in f:
    line = line.strip()
    d = line.split(",")
    fileData.append(float(d[1]))
f.close()


#main data store arrays
data = []

MA7 = []
MA25 = []
MA99 = []
MA250 = []

MA7D = []
MA25D = []
MA99D = []
MA250D = []


#trading values
maxTrades = 20
curTrades = []
comTrades = []

returnThreshold = 0.15
highSell = 0.75

#trading file export
tradeFile = "trad.txt"

#allows enough of an initial buffer to be built (long term integral and differential values)
startTradingPoint = 350




#run calculations
def calculateValues(curPos):

    #generate runningIntegral values
    if(curPos > 8):
        MA7.append(runningIntegral(data[(curPos - 7):(curPos + 1)], 7))
    else:
        MA7.append(None)

    if(curPos > 26):
        MA25.append(runningIntegral(data[(curPos - 25):(curPos + 1)], 25))
    else:
        MA25.append(None)
    
    if(curPos > 100):
        MA99.append(runningIntegral(data[(curPos - 99):(curPos + 1)], 99))
    else:
        MA99.append(None)

    if(curPos > 251):
        MA250.append(runningIntegral(data[(curPos - 250):(curPos + 1)], 250))
    else:
        MA250.append(None)

    
    #generate runningDifferential values
    if(curPos > 13):
        MA7D.append(runningDifferential(MA7[(curPos - 5):(curPos + 1)]))
    else:
        MA7D.append(None)

    if(curPos > 31):
        MA25D.append(runningDifferential(MA25[(curPos - 5):(curPos + 1)]))
    else:
        MA25D.append(None)
    
    if(curPos > 105):
        MA99D.append(runningDifferential(MA99[(curPos - 5):(curPos + 1)]))
    else:
        MA99D.append(None)
    
    if(curPos > 256):
        MA250D.append(runningDifferential(MA250[(curPos - 5):(curPos + 1)]))
    else:
        MA250D.append(None)

#retreive next data value
def getNextValue(curPos):
    global dataAvailable

    #if end of file reached then leave main loop
    if(curPos > (len(fileData) - 2)):
        dataAvailable = False

    #return required data
    return fileData[curPos]

#perform trades
def performTrades(curPos):

    #only perform trades if available
    if(len(curTrades) < maxTrades):

        if(shouldBuy(data, MA7, MA25, MA99, MA250, MA7D, MA25D, MA99D, MA250D, curPos)):
            curTrades.append(curPos)

    else:

        if(shouldSell(data, MA7, MA25, MA99, MA250, MA7D, MA25D, MA99D, MA250D, curPos)):
            
            for t in curTrades:
                percReturn = ((data[curPos] - data[t]) / data[t]) * 100

                if(percReturn > returnThreshold):

                    #append completed trade to list and remove from current list
                    comTrades.append([t, curPos, percReturn])
                    curTrades.remove(t)

                    print("Trade Complete: Buy {:.4f}\tSell {:.4f}\tReturn {:.3f}%".format(data[t], data[curPos], percReturn))



        #check to see if there are any high points to take profit early (in case peak not detected)
        for t in curTrades:
            percReturn = ((data[curPos] - data[t]) / data[t]) * 100

            if(percReturn > highSell):

                #append completed trade to list and remove from current list
                comTrades.append([t, curPos, percReturn])
                curTrades.remove(t)

                print("Trade Complete: Buy {:.4f}\tSell {:.4f}\tReturn {:.3f}%".format(data[t], data[curPos], percReturn))


def clearValues():

    data = []

    MA7 = []
    MA25 = []
    MA99 = []
    MA250 = []

    MA7D = []
    MA25D = []
    MA99D = []
    MA250D = []


def printCurrentTrades():

    print("\nOpen Trades")

    for t in curTrades:
        percReturn = ((data[len(data) - 1] - data[t]) / data[t]) * 100

        print("Buy {:.4f}\tReturn {:.3f}%".format(data[t], percReturn))


def printTotalReturn():

    print("\nReturn Summary")

    highestReturn = 0
    totalReturn = 0

    for t in comTrades:
        totalReturn += t[2]

        if(t[2] > highestReturn):
            highestReturn = t[2]

    print("Number of Trades {}".format(len(comTrades)))
    print("Total Return {:.3f}%".format(totalReturn))
    print("Average Return {:.3f}%".format(totalReturn / len(comTrades)))
    print("Highest Return {:.3f}%".format(highestReturn))

    return totalReturn, highestReturn


def logTrades():

    f = open(tradeFile, "w")

    for t in comTrades:
        f.write("{},{},{:.3f}\n".format(t[0], t[1], t[2]))
    
    f.close()


def setTrading(a):
    setTradingConstants(a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7])



def mainLoop():

    curPos = 0

    print("Completed Trades")

    #main loop function
    while dataAvailable:

        #retrieve next data value (replaced by API function once live)
        data.append(getNextValue(curPos))

        #run calculations
        calculateValues(curPos)

        if(curPos > startTradingPoint):
            performTrades(curPos)

        curPos += 1

    printTradingConstants()
    printCurrentTrades()
    totalReturn, hightestReturn = printTotalReturn()

    logTrades()

    return totalReturn, hightestReturn


if __name__ == "__main__":
    mainLoop()
