#this is the  main trend analysis file



#takes an array (len > size) and finds the integral over the past (size) values
def runningIntegral(data, size):

    lastValue = len(data) - 1
    integralValue = sum(data[(lastValue - size):lastValue]) / size

    return integralValue


#takes an array (len > 2) and finds the differential at the point
def runningDifferential(data, size = 2):

    lastValue = len(data) - 1
    differentialValue = (data[lastValue] - data[lastValue - size]) / 2

    return differentialValue



#takes an array (len > size * 2) of differential data and determines whether it is a peak at (size) before end 
def isPeak(data, size = 1):
    
    lastValue = len(data) - 1

    #positive to negative
    return ((data[lastValue - size] > 0) and (data[lastValue] < 0))


#takes an array (len > size * 2) of differential data and determines whether it is a trough at (size) before end
def isTrough(data, size = 1):

    lastValue = len(data) - 1

    #negative to positive
    return ((data[lastValue - size] < 0) and (data[lastValue] > 0))




#compares two waves and finds the area between then since their last crossover
def areaUnder(data1, data2):
    dataSize = len(data1) - 1

    #takes not of the 
    is1Higher = (data1[dataSize] < data2[dataSize])

    areaTotal = 0

    for i in range(0, len(data1)):

        #checks if paths havent crossed over
        if(is1Higher and (data1[dataSize - (i + 1)] < data2[dataSize - (i + 1)])):

            areaTotal += abs(data1[dataSize - i] - data2[dataSize - i])

        else:
            #return area
            return areaTotal

    return areaTotal


