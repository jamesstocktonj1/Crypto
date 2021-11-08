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



