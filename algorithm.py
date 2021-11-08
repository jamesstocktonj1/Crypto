#this is the main algorithm file which makes the decision whether to (possibly) buy or sell 

from liveAnalysis import *


#trading constants
buyMAThreshold = 2.5
MA99GradientThreshold = -0.1
MA250GradientThreshold = 0.01
buyMA99DifThreshold = 5
buyMA250DifThreshold = 5

sellMAThreshold = 2.5
sellMA99DifThreshold = 5
buyMA250DifThreshold = 5

"""
data used is as followed

data = []

MA7 = []
MA25 = []
MA99 = []
MA250 = []

MA7D = []
MA25D = []
MA99D = []
MA250D = []
"""




def shouldSell(data, MA7, MA25, MA99, MA250, MA7D, MA25D, MA99D, MA250D, curPos):
    sellState = False

    #when MA25 is at a peak and the difference betweeen MA25 and MA99 is large
    sellState = sellState or (isPeak(MA25D) and ((MA25[curPos] - MA99[curPos]) > sellMAThreshold))

    #when MA7 is at a trough and the difference between the current value and MA99 is large
    sellState = sellState or (isPeak(MA7D) and ((data[curPos] - MA99[curPos]) > sellMA99DifThreshold))

    return sellState



def shouldBuy(data, MA7, MA25, MA99, MA250, MA7D, MA25D, MA99D, MA250D, curPos):
    buyState = False

    #when MA25 is at a trough and the difference between MA99 and MA25 is large and also the gradient of MA99 can't be less than a slightly negative slope
    buyState = buyState or (isTrough(MA25D) and ((MA99[curPos] - MA25[curPos]) > buyMAThreshold) and (MA99D[curPos] > MA99GradientThreshold))

    #when MA7 is at a trough and the difference between MA99 and the current value is large
    buyState = buyState or (isTrough(MA7D) and ((MA99[curPos] - data[curPos]) > buyMA99DifThreshold))

    #when MA250 is at a trough
    buyState = buyState or ((abs(MA250D[curPos]) < MA250GradientThreshold) and isTrough(MA25D))
    #buyState = buyState or isTrough(MA250D)

    return buyState