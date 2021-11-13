


from .Algorithm import *
from .Analysis import *


#trading constants
buyMAThreshold = 2.5
MA99GradientThreshold = -0.1
MA250GradientThreshold = 0.05
buyMA99DifThreshold = 5
buyMA250DifThreshold = 5
areaUnderThreshold = 350
buyMA250GradientThreshold = -0.075

sellMAThreshold = 2.5
sellMA99DifThreshold = 5
sellMA250DifThreshold = 5




class SimpleAlgorithm(Algorithm):

    #algorithm design in child class
    def shouldSell(self):
        sellState = False

        #when MA25 is at a peak and the difference betweeen MA25 and MA99 is large
        sellState = sellState or (isPeak(self.MA25D) and ((self.MA25[self.curPos] - self.MA99[self.curPos]) > sellMAThreshold))

        #when MA7 is at a trough and the difference between the current value and MA99 is large
        sellState = sellState or (isPeak(self.MA7D) and ((self.data[self.curPos] - self.MA99[self.curPos]) > sellMA99DifThreshold))

        #when MA250 is at a peak
        #sellState = sellState or ((abs(MA250D[curPos]) < MA250GradientThreshold) and isPeak(MA25D))

        return sellState

    #algorithm design in child class
    def shouldBuy(self):
        buyState = False

        #when MA25 is at a trough and the difference between MA99 and MA25 is large and also the gradient of MA99 can't be less than a slightly negative slope
        buyState = buyState or (isTrough(self.MA25D) and ((self.MA99[self.curPos] - self.MA25[self.curPos]) > buyMAThreshold) and (self.MA99D[self.curPos] > MA99GradientThreshold))

        #when MA7 is at a trough and the difference between MA99 and the current value is large
        buyState = buyState or (isTrough(self.MA7D) and ((self.MA99[self.curPos] - self.data[self.curPos]) > buyMA99DifThreshold))

        #when MA25 is at a trough and the area under the graph is large then buy
        buyState = buyState or (isTrough(self.MA25D) and (areaUnder(self.MA25, self.MA99) > areaUnderThreshold))

        #when MA250 is at a trough
        #buyState = buyState or ((abs(MA250D[curPos]) < MA250GradientThreshold) and isTrough(MA25D))
        #buyState = buyState or isTrough(MA250D)

        buyState = buyState and (self.MA250D[self.curPos] > buyMA250GradientThreshold)

        return buyState


    #returns bool whether a new completed trade has been made
    def newCompleteTrade(self):
        return False

    #returns dictionary entry of completed trade
    def getCompleteTrade(self):
        return None

    #returns array of current trades
    def getCurrentTrades(self):
        return curTrades