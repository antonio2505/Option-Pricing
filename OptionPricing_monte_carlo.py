#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 20:07:26 2022

@author: kassi
"""

import numpy as np
import math 
import time

class OptionPricing:
    def __init__(self,S0,E,T,rf,sigma,iterations):
        self.S0=S0
        self.E = E
        self.T=T
        self.rf=rf
        self.sigma=sigma
        self.iterations=iterations
        
    def call_option_simulation(self):
        #we have 2 columns: first with 0s the second columns will store the payoff
        #we need the first columns of 0s: payoffs function is max(0,S-E) for call option
        option_data=np.zeros([self.iterations,2])
        
        #dimension: 1 dimension array with as many item as the itrations
        rand= np.random.normal(0, 1, [1, self.iterations])
        
        #equation for the S(t) stock price
        stock_price= self.S0*np.exp(self.T*(self.rf-0.5*self.sigma**2)+self.sigma*np.sqrt(self.T)*rand)
        
        #we need S-E because we have to calculate the max(S-E,0)
        option_data[:,1]= stock_price- self.E
        
        #average for the monte-carlo method
        average = np.sum(np.amax(option_data,axis=1))/float(self.iterations)
        
        #We have to use the exp(-rT) discount factor
        return np.exp(-1.0*self.rf*self.T)*average
        
        
        
    def put_option_simulation(self):
        #we have 2 columns: first with 0s the second columns will store the payoff
        #we need the first columns of 0s: payoffs function is max(0,S-E) for call option
        option_data=np.zeros([self.iterations,2])
        
        #dimension: 1 dimension array with as many item as the itrations
        rand= np.random.normal(0,1,[1,self.iterations])
        
        #equation for the S(t) stock price
        stock_price= self.S0*np.exp(self.T*(self.rf-0.5*self.sigma**2)+self.sigma*np.sqrt(self.T)*rand)
        
        #we need S-E because we have to calculate the max(E-S,0)
        option_data[:,1]= self.E - stock_price
        
        #average for the monte-carlo method
        average = np.sum(np.amax(option_data,axis=1))/float(self.iterations)
        
        #We have to use the exp(-rT) discount factor
        return np.exp(-1.0*self.rf*self.T)*average
            
        
if __name__=="__main__":
    
    S0=100
    E=100
    T=1
    rf=0.05
    sigma=0.2
    iterations=10000000
    
    model = OptionPricing(S0,E,T,rf,sigma,iterations)
    print("Call Option Price with Monte-Carlo Approche: ",model.call_option_simulation())
    print("Put Option Price with Monte-Carlo Approche: ",model.put_option_simulation())
    
        
        
        
        
        
        
        