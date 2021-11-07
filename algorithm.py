#this is the main algorithm file which makes the decision whether to (possibly) buy or sell 

from liveAnalysis import *


#trading constants
buyMAThreshold = 2.5
MA99GradientThreshold = -0.13
MA250GradientThreshold = 0
buyMA99DifThreshold = -5

sellMAThreshold = 2.5
sellMA99DifThreshold = 5

"""
data used is as followed

MA7 = []
MA25 = []
MA99 = []
MA250 = []

MA7D = []
MA25D = []
MA99D = []
MA250D = []
"""

def nothingNone(MA7, MA25, MA99, MA250, MA7D, MA25D, MA99D, MA250D, curPos):
    isNone = False
    try:
        isNone = isNone or (None in MA7[curPos])
        isNone = isNone or (None in MA25[curPos])
        isNone = isNone or (None in MA99[curPos])
        isNone = isNone or (None in MA250[curPos])

        isNone = isNone or (None in MA7D[curPos])
        isNone = isNone or (None in MA25D[curPos])
        isNone = isNone or (None in MA99D[curPos])
        isNone = isNone or (None in MA250D[curPos])
    except:
        return False

    return not isNone







def shouldSell(data, MA7, MA25, MA99, MA250, MA7D, MA25D, MA99D, MA250D, curPos):
    sellState = False

    #when there is a peak in MA25 and the difference between MA99 and MA25 is large then stock is potentially bought
    sellState = sellState or (isPeak(MA25D, 1) and ((MA25[curPos] - MA99[curPos]) > sellMAThreshold))

    #the following is a more agressive way of buying/selling but the threshold should be high
    #when there is a peak in MA7 and the difference between MA99 and the trading price is large then stock is potentially bought
    sellState = sellState or (isPeak(MA7D, 1) and ((data[curPos] - MA99[curPos]) > sellMA99DifThreshold))

    return sellState



def shouldBuy(data, MA7, MA25, MA99, MA250, MA7D, MA25D, MA99D, MA250D, curPos):
    buyState = False

    #when there is a trough in MA25 and the difference between MA99 and MA25 is large then stock is potentially bought
    buyState = buyState or (isTrough(MA25D, 1) and ((MA99[curPos] - MA25[curPos]) > buyMAThreshold))

    #the following is a more agressive way of buying/selling but the threshold should be high
    #when there is a trough in MA7 and the difference between MA99 and the trading price is large then stock is potentially bought
    buyState = buyState or (isTrough(MA7D, 1) and ((MA99[curPos] - data[curPos])  < buyMA99DifThreshold))

    return buyState