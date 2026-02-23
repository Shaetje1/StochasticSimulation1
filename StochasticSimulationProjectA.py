# -*- coding: utf-8 -*-
"""
Created on Mon Feb 23 10:03:00 2026

@author: shaew
"""
import math
import numpy
import matplotlib.pyplot as plt

Volatility=0.25
K=100 #Strike price
r=0.04 #Short rate / interest rate

def StockPrice(T,N): #Takes maturity T, Sampling amount N, returns list of Stock prices
    S = [100] #list of Stock prices
    Delta = T/N
    rn = r*Delta
    a = rn - Volatility*math.sqrt(Delta)
    b = rn + Volatility*math.sqrt(Delta)
    Rolling=[]
    for i in range (1,N+1):
        cf = numpy.random.randint(0,2) #cf = Coinflip, (0,2) draws either 0 or 1, never 2
        S.append(S[i-1]*(1+cf*a + (1-cf)*b))
        Rolling.append((sum(S[0:i])/(i)))

    Rolling.append(sum(S)/len(S))
    return S,Rolling

def PlotStock(S,Rolling):
    #T is always 3 anyways
    t = [] #Temporal grid
    for i in range(0,len(S)) :
        t.append(0+i*(3/(len(S)-1)))
    plt.plot(t,S)
    plt.plot(t,Rolling)
    
    #plt.plot(t,[K]*len(S))   #This plots constant line of the starting/Strike price

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
def AvgProfit(N,MC,Print=False): #MC is how many times we monte Carlo simulate to get option price
    Total=0
    for i in range(0,MC):
        S,Rolling=StockPrice(3,N)
        Sample=(S,Rolling)
        Total+=Profit(Sample,Print)
        if Print:
            print(Total/(i+1))
    print("The AVERAGE OPTION PRICE WITH",N,"-SAMPLED AVERAGE WAS CALCULATED TO BE: ", Total/MC)
    return(Total/MC)
        
    
    
    
# =============================================================================
# (S,Rolling)=StockPrice(3,1000) #Makes a sample stock price with 1000 timepoints
# PlotStock(S,Rolling) #Plots it
# Profit((S,Rolling),True) #Calculates the option value in this realization
# =============================================================================
AvgProfit(6,1000)
AvgProfit(36,1000)
AvgProfit(150,1000)
AvgProfit(750,1000)




    