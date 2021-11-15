#parent object oriented trading algorithm implementation


from .Analysis import *


#12 hour buffer size
maxBufferSize = 120 * 60 * 60

uLongDataSize = 2000

class Algorithm:

    


    def __init__(self):

        #data buffer values
        self.data = []

        self.MA7 = []
        self.MA25 = []
        self.MA99 = []
        self.MA250 = []
        self.uLong = []

        self.MA7D = []
        self.MA25D = []
        self.MA99D = []
        self.MA250D = []
        self.uLongD = []

        self.runningAverage = 0
        self.runningRunningAverage = []

        self.curPos = 0
        self.totalPosition = 0

        #trading dictionary format
        #{'openTime': 0, 'closeTime': 0, 'openPrice': 0, 'closeTime': 0, 'percReturn': 0}

        #constant definitions
        self.curTrades = []
        self.comTrades = []

        self.latestOpenTrades = []
        self.latestClosedTrades = []

        self.newCurTrade = False
        self.newComTrade = False

    #resize the buffer
    def resizeBuffer(self):

        if(len(self.data) > maxBufferSize):
            self.data = self.data[(len(self.data) - maxBufferSize):len(self.data)]

            self.MA7 = self.MA7[(len(self.data) - maxBufferSize):len(self.data)]
            self.MA25 = self.MA25[(len(self.data) - maxBufferSize):len(self.data)]
            self.MA99 = self.MA99[(len(self.data) - maxBufferSize):len(self.data)]
            self.MA250 = self.MA250[(len(self.data) - maxBufferSize):len(self.data)]
            self.uLong = self.uLong[(len(self.data) - maxBufferSize):len(self.data)]

            self.MA7D = self.MA7D[(len(self.data) - maxBufferSize):len(self.data)]
            self.MA25D = self.MA25D[(len(self.data) - maxBufferSize):len(self.data)]
            self.MA99D = self.MA99D[(len(self.data) - maxBufferSize):len(self.data)]
            self.MA250D = self.MA250D[(len(self.data) - maxBufferSize):len(self.data)]
            self.uLongD = self.uLongD[(len(self.data) - maxBufferSize):len(self.data)]

            self.curPos = len(self.data) - 1

    #add new current value to the buffer
    def addValue(self, value):
        self.data.append(value)

        self.curPos = len(self.data) - 1
        self.totalPosition += 1

    #run data analysis
    def calculateValues(self):

        #generate runningIntegral values
        if(self.curPos > 8):
            self.MA7.append(runningIntegral(self.data[(self.curPos - 7):(self.curPos + 1)], 7))
        else:
            self.MA7.append(None)

        if(self.curPos > 26):
            self.MA25.append(runningIntegral(self.data[(self.curPos - 25):(self.curPos + 1)], 25))
        else:
            self.MA25.append(None)
        
        if(self.curPos > 100):
            self.MA99.append(runningIntegral(self.data[(self.curPos - 99):(self.curPos + 1)], 99))
        else:
            self.MA99.append(None)

        if(self.curPos > 251):
            self.MA250.append(runningIntegral(self.data[(self.curPos - 250):(self.curPos + 1)], 250))
        else:
            self.MA250.append(None)

        if(self.curPos > (uLongDataSize + 1)):
            self.uLong.append(runningIntegral(self.data[(self.curPos - uLongDataSize):(self.curPos + 1)], uLongDataSize))
        else:
            self.uLong.append(None)

        
        #generate runningDifferential values
        if(self.curPos > 13):
            self.MA7D.append(runningDifferential(self.MA7[(self.curPos - 5):(self.curPos + 1)]))
        else:
            self.MA7D.append(None)

        if(self.curPos > 31):
            self.MA25D.append(runningDifferential(self.MA25[(self.curPos - 5):(self.curPos + 1)]))
        else:
            self.MA25D.append(None)
        
        if(self.curPos > 105):
            self.MA99D.append(runningDifferential(self.MA99[(self.curPos - 5):(self.curPos + 1)]))
        else:
            self.MA99D.append(None)
        
        if(self.curPos > 256):
            self.MA250D.append(runningDifferential(self.MA250[(self.curPos - 5):(self.curPos + 1)]))
        else:
            self.MA250D.append(None)

        if(self.curPos > (uLongDataSize + 6)):
            self.uLongD.append(runningDifferential(self.uLong[(self.curPos - 5):(self.curPos + 1)]))
        else:
            self.uLongD.append(None)

        self.runningAverage = sum(self.data) / len(self.data)
        self.runningRunningAverage.append(self.runningAverage)


    #algorithm design in child class
    def shouldSell(self):
        return False

    #algorithm design in child class
    def shouldBuy(self):
        return False


    #executes the trading algorithm
    def executeTrade(self):
        pass

    #gets the latest open trades
    def getLatestOpenTrades(self):
        return self.latestOpenTrades

    #gets the latest closed trades
    def getLatestClosedTrades(self):
        return self.latestClosedTrades

    #returns bool whether a new completed trade has been made
    def newCompleteTrade(self):
        return self.newComTrade

    #returns dictionary entry of completed trade
    def getCompleteTrade(self):
        return self.comTrades
        
    #returns bool whether a new trade should currently be open
    def newCurrentTrade(self):
        return self.newCurTrade

    #returns array of current trades
    def getCurrentTrades(self):

        for t in self.curTrades:
            percReturn = ((self.data[self.curPos] - t['openPrice']) / t['openPrice']) * 100

            self.curTrades[self.curTrades.index(t)]['percReturn'] = percReturn

        return self.curTrades


    def getVolatilityValue(self):
        volatilityScope = 5000

        if(self.totalPosition < volatilityScope):
            return (max(self.data[:(self.curPos + 1)]) - min(self.data[:(self.curPos + 1)])) / min(self.data[:(self.curPos + 1)])
        else:
            return (max(self.data[(self.curPos - volatilityScope):(self.curPos + 1)]) - min(self.data[(self.curPos - volatilityScope):(self.curPos + 1)])) / min(self.data[(self.curPos - volatilityScope):(self.curPos + 1)])