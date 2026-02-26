# -*- coding: utf-8 -*-
"""
Created on Mon Feb 23 10:03:00 2026

@author: shaew
"""
import math
import numpy
import matplotlib.pyplot as plt
import time
#numpy.random.seed(10) To generate the same results each time
AmountOfBlackScholesSamples=4500 #Number should me a multiple of 4500
Volatility=0.25
K=100 #Strike price
r=0.04 #Short rate / interest rate

def StockPrice(T): #Returns list of Stock Prices based on discrete BS-Model
    S = [100]
    Delta = T/AmountOfBlackScholesSamples
    rn = r*Delta
    a = rn - Volatility*math.sqrt(Delta)
    b = rn + Volatility*math.sqrt(Delta)
    for i in range (1,AmountOfBlackScholesSamples+1):
        cf = numpy.random.randint(0,2) #cf = Coinflip, (0,2) draws either 0 or 1, never 2
        S.append(S[i-1]*(1+cf*a + (1-cf)*b))
    return S

def CalcRolling(S,N) :
    RollingAvg=[]
    for i in range(0,AmountOfBlackScholesSamples+1,int(AmountOfBlackScholesSamples/N)):
        RollingAvg.append(sum(S[0:i+1:int(AmountOfBlackScholesSamples/N)]))
        Idx=int(i*N/AmountOfBlackScholesSamples)
        RollingAvg[Idx]=RollingAvg[Idx]/len(RollingAvg)
    
    return RollingAvg

def PlotStock(S,RollingAvg):
    #T is always 3 anyways
    t = [] #Temporal grid
    for i in range(0,len(S)) :
        t.append(0+i*(3/(len(S)-1)))
    plt.plot(t,S)
    tRolling=[] #temporal grid for rolling average (less data points)
    for i in range(0,len(RollingAvg)) :
        tRolling.append(0+i*(3/(len(RollingAvg)-1)))
    plt.plot(tRolling,RollingAvg)
    
    #plt.plot(tRolling,[K]*len(tRolling))   #This plots constant line of the starting/Strike price

def Profit(Sample,Print=False):
    Profit=Sample[1][-1]-K
    if Profit>0:
        if Print:
            print("You made",Profit,"Profit :D!")
        return Profit
    else:
        if Print:
            print("The option went out of the money :(")
        return 0

    
def GenSamples(amount):
    Samples=[]
    for i in range(0,amount):
        Samples.append(StockPrice(3))
    return Samples

def AvgProfit(N,Samples,Print=False,a=True): 
    Total=0
    for i in Samples:
        RollingAvg=CalcRolling(i,N)
        Total+=Profit((i,RollingAvg))
        if Print:
            print(Total/(i+1))
    if a:
        print("The AVERAGE OPTION PRICE WITH N =",N,"WAS CALCULATED TO BE: ", Total/len(Samples))
    return(Total/len(Samples))
        
    
    
    

#This block just generates 1 sample, then calculates the rolling average and plots, for testing purposes
# =============================================================================
# S=StockPrice(3)
# RollingAvg=CalcRolling(S,6) #Makes a sample stock price with average sampling 
# PlotStock(S,RollingAvg) #Plots it
# Profit((S,RollingAvg),True) #Calculates the option value in this realization
# =============================================================================



#This block Generates samples, then calculates the average profit with different sampling times
a=time.perf_counter()
Samples=GenSamples(100)
x=[2,3,6,12,15,36,90,150,300,750,2250,4500]
y=[]
y.append(AvgProfit(2,Samples))
y.append(AvgProfit(3,Samples))
y.append(AvgProfit(6,Samples))
y.append(AvgProfit(12,Samples))
y.append(AvgProfit(15,Samples))
y.append(AvgProfit(36,Samples))
y.append(AvgProfit(90,Samples))
y.append(AvgProfit(150,Samples))
y.append(AvgProfit(300,Samples))
y.append(AvgProfit(750,Samples))
y.append(AvgProfit(2250,Samples))
y.append(AvgProfit(4500,Samples))
y=[i-y[-1] for i in y]
plt.plot(x,y,'r')
alpha=2/3
z=[-i**(-alpha) for i in x]
plt.plot(x,z,'b')
alpha=0.9
z=[-i**(-alpha) for i in x]
plt.plot(x,z,'b')

print("Program took",time.perf_counter()-a,"seconds to run")






    