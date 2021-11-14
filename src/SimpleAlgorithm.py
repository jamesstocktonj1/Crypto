


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


#trading values
maxTrades = 20
curTrades = []
comTrades = []

#buy conditions
returnThreshold = 0.5
highSell = 0.85
buyBuyCooloff = 30

#sellconditions
lowSell = -2.0
longSellTime = 5000
longSellReturn = 0.1
buySellCooloff = 600


#allows enough of an initial buffer to be built (long term integral and differential values)
startTradingPoint = 350


class SimpleAlgorithm(Algorithm):

    
    def shouldSell(self):
        sellState = False

        #when MA25 is at a peak and the difference betweeen MA25 and MA99 is large
        sellState = sellState or (isPeak(self.MA25D) and ((self.MA25[self.curPos] - self.MA99[self.curPos]) > sellMAThreshold))

        #when MA7 is at a trough and the difference between the current value and MA99 is large
        sellState = sellState or (isPeak(self.MA7D) and ((self.data[self.curPos] - self.MA99[self.curPos]) > sellMA99DifThreshold))

        #when MA250 is at a peak
        #sellState = sellState or ((abs(MA250D[curPos]) < MA250GradientThreshold) and isPeak(MA25D))

        return sellState

    
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



    def executeTrade(self):

        self.latestOpenTrades = []
        self.latestClosedTrades = []

        self.newCurTrade = False
        self.newComTrade = False

        if(self.totalPosition < startTradingPoint):
            return None


        #check buy conditions
        if(self.shouldBuy()):

            if(len(self.curTrades) > 0):

                #if there are more than one trade and it is after (buyCooloff) amount of time
                if(((self.totalPosition - self.curTrades[len(self.curTrades) - 1]['openTime']) > buyBuyCooloff) and (len(self.curTrades) < maxTrades)):

                    if(len(self.comTrades) == 0):
                        self.curTrades.append({'openTime': self.totalPosition, 'closeTime': 0, 'openPrice': self.data[self.curPos], 'closePrice': 0, 'percReturn': 0})

                        self.latestOpenTrades.append({'openTime': self.totalPosition, 'closeTime': 0, 'openPrice': self.data[self.curPos], 'closePrice': 0, 'percReturn': 0})

                    
                    elif(((self.totalPosition - self.comTrades[len(self.comTrades) - 1]['closeTime']) > buySellCooloff)):
                        self.curTrades.append({'openTime': self.totalPosition, 'closeTime': 0, 'openPrice': self.data[self.curPos], 'closePrice': 0, 'percReturn': 0})

                        self.latestOpenTrades.append({'openTime': self.totalPosition, 'closeTime': 0, 'openPrice': self.data[self.curPos], 'closePrice': 0, 'percReturn': 0})

            else:

                #perform trade if curTrades is equal to 0
                self.curTrades.append({'openTime': self.totalPosition, 'closeTime': 0, 'openPrice': self.data[self.curPos], 'closePrice': 0, 'percReturn': 0})

                self.latestOpenTrades.append({'openTime': self.totalPosition, 'closeTime': 0, 'openPrice': self.data[self.curPos], 'closePrice': 0, 'percReturn': 0})


        if(self.shouldSell()):
            
            for t in self.curTrades:
                percReturn = ((self.data[self.curPos] - t['openPrice']) / t['openPrice']) * 100

                if(percReturn > returnThreshold):

                    #append completed trade to list and remove from current list
                    self.comTrades.append({'openTime': t['openTime'], 'closeTime': self.totalPosition, 'openPrice': t['openPrice'], 'closePrice': self.data[self.curPos], 'percReturn': percReturn})

                    self.latestClosedTrades.append({'openTime': t['openTime'], 'closeTime': self.totalPosition, 'openPrice': t['openPrice'], 'closePrice': self.data[self.curPos], 'percReturn': percReturn})

                    self.curTrades.remove(t)


                elif(percReturn > highSell):

                    #append completed trade to list and remove from current list
                    self.comTrades.append({'openTime': t['openTime'], 'closeTime': self.totalPosition, 'openPrice': t['openPrice'], 'closePrice': self.data[self.curPos], 'percReturn': percReturn})

                    self.latestClosedTrades.append({'openTime': t['openTime'], 'closeTime': self.totalPosition, 'openPrice': t['openPrice'], 'closePrice': self.data[self.curPos], 'percReturn': percReturn})
                    
                    self.curTrades.remove(t)

                
                #stop long term loss
                elif(((self.totalPosition - t['openTime']) > longSellTime) and (percReturn > 0.1)):

                    #append completed trade to list and remove from current list
                    self.comTrades.append({'openTime': t['openTime'], 'closeTime': self.totalPosition, 'openPrice': t['openPrice'], 'closePrice': self.data[self.curPos], 'percReturn': percReturn})

                    self.latestClosedTrades.append({'openTime': t['openTime'], 'closeTime': self.totalPosition, 'openPrice': t['openPrice'], 'closePrice': self.data[self.curPos], 'percReturn': percReturn})
                    
                    self.curTrades.remove(t)

                #stop loss
                elif(percReturn < lowSell):

                    #append completed trade to list and remove from current list
                    self.comTrades.append({'openTime': t['openTime'], 'closeTime': self.totalPosition, 'openPrice': t['openPrice'], 'closePrice': self.data[self.curPos], 'percReturn': percReturn})

                    self.latestClosedTrades.append({'openTime': t['openTime'], 'closeTime': self.totalPosition, 'openPrice': t['openPrice'], 'closePrice': self.data[self.curPos], 'percReturn': percReturn})
                    
                    self.curTrades.remove(t)


        #set new trade flags
        self.newCurTrade = len(self.latestOpenTrades) != 0
        self.newComTrade = len(self.latestClosedTrades) != 0




    
    def getCompleteTrade(self):
        return None

