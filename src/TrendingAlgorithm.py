from .Algorithm import *
from .Analysis import *


startTradingPoint = 1000
buyDataAverageDifference = 0.25
averageGradientThreshold = 0.1

highSell = 0.8
lowSell = -10.0

buyBuyCooloff = 300


class TrendingAlgorithm(Algorithm):



    def __init__(self):

        #data buffer values
        self.data = []

        self.MA25 = []
        self.MA25D = []

        self.runningRunningAverage = []
        self.runningAverageD = []

        self.curPos = 0
        self.totalPosition = 0


        #trading definitions
        self.curTrades = []
        self.comTrades = []

        self.latestOpenTrades = []
        self.latestClosedTrades = []

        self.newCurTrade = False
        self.newComTrade = False


    def resizeBuffer(self):

        if(len(self.data) > (4 * maxBufferSize)):
            self.data = self.data[maxBufferSize:]

            self.MA25 = self.MA25[maxBufferSize:]
            self.MA25D = self.MA25D[maxBufferSize:]

            self.curPos = len(self.data) - 1
    

    def calculateValues(self):

        if(self.curPos > 99):
            self.MA25.append(runningIntegral(self.data[(self.curPos - 99):], 99))
        else:
            self.MA25.append(self.data[self.curPos])
    
        if(self.curPos > 120):
            self.MA25D.append(runningDifferential(self.MA25[(self.curPos - 5):]))
        else:
            self.MA25D.append(None)

        if(self.curPos < runningAverageLength):
            self.runningRunningAverage.append(sum(self.data) / len(self.data))
        else:
            self.runningRunningAverage.append(sum(self.data[(self.curPos - runningAverageLength):]) / len(self.data[(self.curPos - runningAverageLength):]))

        if(self.curPos > 50):
            self.runningAverageD.append(runningDifferential(self.runningRunningAverage[(self.curPos - 50):], size=50))
        else:
            self.runningAverageD.append(None)

    
    def shouldSell(self):
        sellState = False

        sellState = sellState or (isPeak(self.MA25D) and (self.data[self.curPos] > self.runningRunningAverage[self.curPos]))

        #sellState = sellState 

        return sellState

    def shouldBuy(self):
        buyState = False

        buyState = buyState or isTrough(self.MA25D)

        buyState = buyState and (self.data[self.curPos] < (self.runningRunningAverage[self.curPos] * (1 - (buyDataAverageDifference * 0.01))))

        buyState = buyState or (self.data[self.curPos] < (self.runningRunningAverage[self.curPos] * (1 - (buyDataAverageDifference * 0.2))))

        #buyState = buyState and (self.runningAverageD[self.curPos] > 0)

        #buyState = buyState and (self.getVolatilityValue() < 0.5)

        return buyState


    def openTrade(self):

        tempTrade = {'openTime': self.totalPosition, 
                     'closeTime': 0, 
                     'openPrice': self.data[self.curPos], 
                     'closePrice': 0, 
                     'percReturn': 0}

        self.curTrades.append(tempTrade)

        self.latestOpenTrades.append(tempTrade)

    def closeTrade(self, trade):

        percReturn = ((self.data[self.curPos] - trade['openPrice']) / trade['openPrice']) * 100

        tempTrade = {'openTime': trade['openTime'], 
                     'closeTime': self.totalPosition, 
                     'openPrice': trade['openPrice'], 
                     'closePrice': self.data[self.curPos], 
                     'percReturn': percReturn}

        self.comTrades.append(tempTrade)

        self.latestClosedTrades.append(tempTrade)

        self.curTrades.remove(trade)


    def executeTrade(self):

        self.latestOpenTrades = []
        self.latestClosedTrades = []

        self.newCurTrade = False
        self.newComTrade = False

        if(self.totalPosition < startTradingPoint):
            return None

        
        if((self.data[self.curPos] < self.runningRunningAverage[self.curPos]) and self.shouldBuy()):

            if(len(self.curTrades) != 0):
                
                if((self.totalPosition - self.curTrades[len(self.curTrades) - 1]['openTime']) > buyBuyCooloff):
                    self.openTrade()

            else:
                self.openTrade()


        if((self.data[self.curPos] > self.runningRunningAverage[self.curPos]) and self.shouldSell() and (len(self.curTrades) != 0)):

            for t in self.curTrades:

                percReturn = ((self.data[self.curPos] - t['openPrice']) / t['openPrice']) * 100
                try:
                    preReturn = ((self.runningRunningAverage[t['openTime']] - self.data[t['openTime']]) / self.data[t['openTime']]) * 100
                except:
                    preReturn = 0
                postReturn = ((self.data[self.curPos] - self.runningRunningAverage[self.curPos]) / self.runningRunningAverage[self.curPos]) * 100

                if((postReturn > preReturn) and (percReturn > 0.05)):

                    self.closeTrade(t)

                elif(percReturn > highSell):
                    
                    self.closeTrade(t)

                elif(percReturn < lowSell):

                    self.closeTrade(t)

        #set new trade flags
        self.newCurTrade = len(self.latestOpenTrades) != 0
        self.newComTrade = len(self.latestClosedTrades) != 0