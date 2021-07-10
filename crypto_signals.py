# -*- coding: utf-8 -*-
"""
Created on Wed Jun 23 15:06:46 2021

@author: mraslan
"""

from tradingview_ta import TA_Handler, Interval, Exchange
import time
import pandas as pd
from datetime import datetime

import ccxt


def Get_symbols(Type):
    ex=ccxt.binance()
    ex.load_markets()
    f=pd.DataFrame(ex.fetch_markets())
    symbs=f[f['active']==True].symbol.unique()
    s=[]
    u=[]
    for symbol in symbs:
        if symbol.split('/')[1]=='BTC':
            s.append(symbol)
        if symbol.split('/')[1]=='USDT':
            u.append(symbol)
    
    if Type=='Future':
        ex = ccxt.binance({
      
        'enableRateLimit': True,
        'options': {
            'defaultType': 'future',  # ←-------------- quotes and 'future'
        },
        })
        
        f=pd.DataFrame(ex.fetch_markets())
        symbs=f[f['active']==True].symbol.unique()
        symm=[]
        for i in range(0,len(symbs)):
            #if symbols[i] not in a:
                symbs[i]=symbs[i].replace('/','')
        nam='BINANCE:'
        pr='PERP'
        symbols=[]
        for symbol in symbs:
                
                symbols.append(nam+symbol+pr)
    
    
    elif Type=='BTC':
        z=s   
        symbo=[]   
        for i in z:
            if "DOWN/" in i or 'UP/' in i or 'BULL/' in i or 'BEAR/' in i:
                t=1
               
            else:
                t=-1
                symbo.append(i)
        symbols=[]
        symm=[]
        for i in range(0,len(symbo)):
            #if symbols[i] not in a:
                symbo[i]=symbo[i].replace('/','')
        a=['PAXUSDT','TUSDUSDT','USDCUSDT','BUSDUSDT','PAXGUSDT','EURUSDT','SUSDUSDT','GBPUSDT','YOYOWBTC']
        nam='BINANCE:'
        for symbol in symbo:
            if symbol not in a:
                symbols.append(nam+symbol)
                symm.append(symbol)
   
    elif Type=='USDT':
        z=u
        symbo=[]   
        for i in z:
            if "DOWN/" in i or 'UP/' in i or 'BULL/' in i or 'BEAR/' in i:
                t=1
               
            else:
                t=-1
                symbo.append(i)
        symbols=[]
        symm=[]
        for i in range(0,len(symbo)):
            #if symbols[i] not in a:
                symbo[i]=symbo[i].replace('/','')
        a=['PAXUSDT','TUSDUSDT','USDCUSDT','BUSDUSDT','PAXGUSDT','EURUSDT','SUSDUSDT','GBPUSDT']
        nam='BINANCE:'
        for symbol in symbo:
            if symbol not in a:
                symbols.append(nam+symbol)
                symm.append(symbol)
        

    return symbols
            

    