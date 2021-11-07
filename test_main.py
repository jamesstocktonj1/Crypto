#test algorithms here from files generated


from liveAnalysis import *
import matplotlib.pyplot as plt


fileName = "dump5.txt"
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

MA99Dif = []


fig1 = plt.subplot(1, 1, 1)
#fig2 = plt.subplot(2, 1, 2)


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
        MA99Dif.append(dataBuf[curPos] - MA99[curPos])
    else:
        MA99.append(None)
        MA99Dif.append(None)

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



    if(curPos > 105):
        
        #when there is a trough in MA25 and the difference between MA99 and MA25 is large then stock is potentially bought
        if(isTrough(MA25D, 1) and ((MA99[curPos] - MA25[curPos]) > buyMAThreshold)):

            print("Buy at {:.4f}".format(dataBuf[curPos]))
            fig1.annotate('B', xy=(curPos, dataBuf[curPos]), verticalalignment='bottom')

        #"..."
        if(isPeak(MA25D, 1) and ((MA25[curPos] - MA99[curPos]) > sellMAThreshold)):
            print("Sell at {:.4f}".format(dataBuf[curPos]))

            fig1.annotate('S', xy=(curPos, dataBuf[curPos]), verticalalignment='bottom')

        #the following is a more agressive way of buying/selling but the threshold should be high
        #when there is a peak in MA7 and the difference between MA99 and the trading price is large then stock is potentially bought
        if(isTrough(MA7D, 1) and (MA99Dif[curPos] < buyMA99DifThreshold)):
            print("Big Dif Buy at {:.4f}".format(dataBuf[curPos]))

            fig1.annotate('B', xy=(curPos, dataBuf[curPos]), verticalalignment='bottom')

        #"..."
        if(isPeak(MA7D, 1) and (MA99Dif[curPos] > sellMA99DifThreshold)):
            print("Big Dif Sell at {:.4f}".format(dataBuf[curPos]))

            fig1.annotate('S', xy=(curPos, dataBuf[curPos]), verticalalignment='bottom')

    #plt.pause(0.01)



fig1.plot(range(0, len(dataBuf)), dataBuf)
fig1.plot(range(0, len(MA25)), MA25)
fig1.plot(range(0, len(MA99)), MA99)
fig1.plot(range(0, len(MA250)), MA250)

#fig2.plot(range(0, len(MA99Dif)), MA99Dif)


plt.show()