#test algorithms here from files generated


from liveAnalysis import *
from algorithm import *
import matplotlib.pyplot as plt


fileName = "dump.txt"
data = []



#load data
f = open(fileName, "r")

for line in f:
    line = line.strip()
    d = line.split(",")
    data.append(float(d[1]))

f.close()



#trading constants
buyMAThreshold = 2.5
MA99GradientThreshold = -0.13
MA250GradientThreshold = 0
buyMA99DifThreshold = -5

sellMAThreshold = 2.5
sellMA99DifThreshold = 5




dataBuf = []

MA7 = []
MA25 = []
MA99 = []
MA250 = []

MA7D = []
MA25D = []
MA99D = []
MA250D = []


fig1 = plt.subplot(1, 1, 1)
#fig2 = plt.subplot(2, 1, 2)


#used for calculating rough profits
numTrades = 0
buyPrice = []
trades = []
curTrade = 0


#a for loop is used to simulate real time trading values coming in

#main function loop
for n in range(0, len(data)):

    d = data[n]    

    dataBuf.append(d)

    curPos = len(dataBuf) - 1

    #generate runningIntegral values
    if(curPos > 8):
        MA7.append(runningIntegral(dataBuf[(curPos - 7):(curPos + 1)], 7))
    else:
        MA7.append(None)

    if(curPos > 26):
        MA25.append(runningIntegral(dataBuf[(curPos - 25):(curPos + 1)], 25))
    else:
        MA25.append(None)
    
    if(curPos > 100):
        MA99.append(runningIntegral(dataBuf[(curPos - 99):(curPos + 1)], 99))
    else:
        MA99.append(None)

    if(curPos > 251):
        MA250.append(runningIntegral(dataBuf[(curPos - 250):(curPos + 1)], 250))
    else:
        MA250.append(None)

    #fig1.plot(range(0, curPos + 1), dataBuf)
    #fig1.plot(range(0, curPos + 1), MA25)
    #fig1.plot(range(0, curPos + 1), MA99)
    #fig1.plot(range(0, curPos + 1), MA250)

    #fig1.plot(range(0, len(dataBuf)), dataBuf)
    #fig1.plot(range(0, len(MA25)), MA25)
    #fig1.plot(range(0, len(MA99)), MA99)
    #fig1.plot(range(0, len(MA250)), MA250)




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


    if(curPos > 205):
        
        #when there is a trough in MA25 and the difference between MA99 and MA25 is large then stock is potentially bought
        if(shouldBuy(dataBuf, MA7, MA25, MA99, MA250, MA7D, MA25D, MA99D, MA250D, curPos)):

            print("Buy at {:.4f}".format(dataBuf[curPos]))
            #fig1.annotate('B', xy=(curPos, dataBuf[curPos]), verticalalignment='bottom')

            if(numTrades < 4):

                numTrades += 1
                buyPrice.append(curPos)

                fig1.annotate("Buy {}".format(numTrades), xy=(curPos, dataBuf[curPos]), verticalalignment='bottom')



        #"..."
        if(shouldSell(dataBuf, MA7, MA25, MA99, MA250, MA7D, MA25D, MA99D, MA250D, curPos)):
            print("Sell at {:.4f}".format(dataBuf[curPos]))

            #fig1.annotate('S', xy=(curPos, dataBuf[curPos]), verticalalignment='bottom')

            if(numTrades > 0):

                for p in buyPrice:

                    percReturn = ((dataBuf[curPos] - dataBuf[p]) / dataBuf[p]) * 100

                    if(percReturn > 0.05):

                        trades.append([p, curPos, percReturn])

                        fig1.annotate("Sell {}".format(buyPrice.index(p)), xy=(curPos, dataBuf[curPos]), verticalalignment='bottom')

                        #fig1.plot([p, curPos], [dataBuf[p], dataBuf[curPos]])

                        numTrades -= 1
                        buyPrice.remove(p)

        if(numTrades > 0):

            for p in buyPrice:

                percReturn = ((dataBuf[curPos] - p) / p) * 100

                if(percReturn < -1.0):
                    pass
                    #print("Stop Loss -1.0%")
                elif(percReturn < -0.5):
                    pass
                    #print("Stop Loss -0.5%")
                """elif(percReturn < -0.25):
                    print("Stop Loss -0.25%")
                elif(percReturn < -0.1):
                    print("Stop Loss -0.1%")"""


    #plt.pause(0.01)



fig1.plot(range(0, len(dataBuf)), dataBuf, label='ETH')
fig1.plot(range(0, len(MA25)), MA25, label='MA25')
fig1.plot(range(0, len(MA99)), MA99, label='MA99')
fig1.plot(range(0, len(MA250)), MA250, label='MA250')

plt.legend()

#fig2.plot(range(0, len(MA99Dif)), MA99Dif)


for t in trades:
    print("Buy: {:.4f}\tSell: {:.4f}\tReturn: {:.2f}".format(float(dataBuf[t[0]]), float(dataBuf[t[1]]), float(t[2])))
    fig1.plot([t[0], t[1]], [dataBuf[t[0]], dataBuf[t[1]]], label="Return {:.2f}%".format(t[2]))

plt.legend()

if(numTrades > 0):
    for t in buyPrice:
        print("Mid-Trade Buy: {:.4f}".format(dataBuf[t]))


plt.show()