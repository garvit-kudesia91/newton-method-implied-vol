# -*- coding: utf-8 -*-
"""
Created on Thu Mar 29 11:39:05 2018

@author: garvit
"""

import scipy.stats as ss
from decimal import Decimal
import math as m
import numpy as np
from datetime import date,timedelta
from mibian import BS

def call_bsm (S0,K,r,T,Otype,sig):
    d1 = Decimal(m.log(S0/K)) + (r+ (sig*sig)/2)*T/(sig*Decimal(m.sqrt(T)))
    d2 = d1 - sig*Decimal(m.sqrt(T))
    if (Otype == "Call"):
        price = S0*Decimal(ss.norm.cdf(np.float(d1))) \
        - K*Decimal(m.exp(-r*T))*Decimal(ss.norm.cdf(np.float(d2)))
        return (price)
    elif (Otype == "Put"):
        price  = -S0*Decimal(ss.norm.cdf(np.float(-d1)))\
        + K*Decimal(m.exp(-r*T))*Decimal(ss.norm.cdf(np.float(-d2)))
        return (price)

def vega (S0,K,r,T,sig):
    d1 = Decimal(m.log(S0/K))/(sig*Decimal(m.sqrt(T))) + Decimal((r+ (sig*sig)/2)*T/(sig*Decimal(m.sqrt(T))))
    vega = S0*Decimal(ss.norm.pdf(np.float(d1)))*Decimal(m.sqrt(T))
    return(vega)
    
    
def imp_vol(S0, K, T, r, market,flag):
    e = 10e-15; x0 = Decimal(1);  
    def newtons_method(S0, K, T, r, market,flag,x0, e):
        delta = call_bsm (S0,K,r,T,flag,x0) - market
        while delta > e:
            x0 = Decimal(x0 - (call_bsm (S0,K,r,T,flag,x0) - market)/vega (S0,K,r,T,x0))
            delta = abs(call_bsm (S0,K,r,T,flag,x0) - market)
        return(Decimal(x0))
    sig =  newtons_method(S0, K, T, r, market,flag,x0 , e)   
    return(sig*100)
    

fromdate = date(2018,3,30)
todate = date(2018,9,21)
daygenerator = (fromdate + timedelta(x + 1) for x in range((todate - fromdate).days))
days = sum(1 for day in daygenerator if day.weekday())
T = Decimal(days)/Decimal(360)    
S0 = Decimal(109.97)
K = Decimal(100)
market = Decimal(13.725)
flag = 'Call'
r = Decimal(0.0225)
iv = imp_vol(S0, K, T, r, market,flag)
print("")
print("")
print("############################ Newton Raphson Method ####################")
print("")
print('The implied volatility from my calculation is',iv,"%")
cp_iv = call_bsm(S0,K,r,T,Otype="Call",sig=Decimal(iv/100))
print('Newton Raphson implied volatility gives call price',cp_iv)
print("Error in obtained call price", '{:.20f}'.format(np.float(market - cp_iv)))
# Mibian Library
c = BS([S0, K, r, days], callPrice=market)
print("")
print("")
print("############################ Bisection Method #########################")
print("")
print("The implied volatility using Mibian Library is", c.impliedVolatility,"%")
cp_mbian = call_bsm(S0,K,r,T,Otype="Call",sig=Decimal(c.impliedVolatility/100))
print('Mibian implied volatility gives call price',cp_mbian)
print("Error in obtained call price", market - cp_mbian)
