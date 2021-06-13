# -*- coding: utf-8 -*-
"""
Created on Thu Jun 10 16:00:38 2021

@author: mraslan
"""

import streamlit as st
import pandas as pd
import ccxt
import numpy as np
from datetime import datetime
from streamlit import caching
import talib
import ccxt
import pandas as pd
import datetime
import numpy as np
import TAcharts
from tapy import Indicators
import ta_py as ta;
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
from backtesting.lib import crossover,cross,resample_apply
def direction_strategy(ratingTotal, ratingOther, ratingMA):
    StrongBound = 0.5
    WeakBound = 0.1
    tradeSignal = getSignal(ratingTotal, ratingOther, ratingMA)
    if tradeSignal>StrongBound:
        strategy='long'
    elif tradeSignal<WeakBound:
        strategy='short'
    else:
        strategy='no action'
    return strategy
def calcRatingAll(df):
    close=df['Close']
    high=df['High']
    low=df['Low']
    volume=df['Volume']
    SMA10 = talib.SMA(close, 10)
    SMA20 = talib.SMA(close, 20)
    SMA30 = talib.SMA(close, 30)
    SMA50 = talib.SMA(close, 50)
    SMA100 = talib.SMA(close, 100)
    SMA200 = talib.SMA(close, 200)

    EMA10 = talib.EMA(close, 10)
    EMA20 = talib.EMA(close, 20)
    EMA30 = talib.EMA(close, 30)
    EMA50 = talib.EMA(close, 50)
    EMA100 = talib.EMA(close, 100)
    EMA200 = talib.EMA(close, 200)

    HullMA9=ta.hull(close, 9)
    # Volume Weighted Moving Average (VWMA)

    d=[close,volume]
    VWMA=ta.vwma(d, 20)
    #[IC_CLine, IC_BLine, IC_Lead1, IC_Lead2] = ichimoku_cloud()

    i= Indicators(df)
    i.ichimoku_kinko_hyo(period_tenkan_sen=9, period_kijun_sen=26, period_senkou_span_b=52, column_name_chikou_span='chikou_span', column_name_tenkan_sen='IC_CLine', column_name_kijun_sen='IC_BLine', column_name_senkou_span_a='IC_Lead1', column_name_senkou_span_b='IC_Lead2')


    IC_CLine=i.df['IC_CLine']
    IC_BLine=i.df['IC_BLine']
    IC_Lead1=i.df['IC_Lead1']
    IC_Lead2=i.df['IC_Lead2']

    # Momentum
    Mom = talib.MOM(close, 10)
    #Moving Average Convergence/Divergence, MACD

    macdMACD, signalMACD, macdhist = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
    # Stochastic RSI
    Stoch_RSI_K, RSI = talib.STOCHRSI(close, timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0)
    # Williams Percent Range

    WR=talib.WILLR(high, low, close, timeperiod=14)

    # Bull / Bear Power
    BullPower = high - talib.EMA(close, 13)
    BearPower = low - talib.EMA(close, 13)
    # Ultimate Oscillator
    UO = talib.ULTOSC(high, low, close,7,14,28)
    #if no isnull(UO):
    UO = UO * 100
    # Relative Strength Index, RSI
    RSI = talib.RSI(close,14)
    # Stochastic
    length = 14
    smoothk = 1
    smoothd = 3

    array=[high,close, low]
    #kStoch=talib.SMA(ta.stoch(array, length), smoothk);

    #dStoch = talib.SMA(kStoch, smoothd)
    #kStoch=st[0][0]
    #dStoch=st[0][1]
    #kStoch = talib.SMA(talib.STOCH(high, low, close, lengthStoch,5,0,3,0), smoothKStoch)
    #dStoch = talib.SMA(kStoch, smoothDStoch)

    #Commodity Channel Index, CCI
    CCI = talib.CCI(high, low, close, timeperiod=20)
    # Awesome Oscillator
    shortlength=5   
    longlength=35
    a=[high,low]
    ao=ta.ao(a, shortlength, longlength);
    # Average Directional Index
    ADX=talib.ADX(high, low, close, timeperiod=14)
    V = talib.ADX(high, low, close, timeperiod=14)
    P = talib.PLUS_DI(high, low, close, timeperiod=14)

    M = talib.MINUS_DI(high, low, close, timeperiod=14)
    adxValue = V
    adxPlus = P
    adxMinus = M

    PriceAvg = talib.EMA(close, 50)
    DownTrend = close < PriceAvg
    UpTrend = close > PriceAvg
    # calculate trading recommendation based on SMA/EMA
    ratingMA = 0
    ratingMAC = 0
    if len(SMA10):
        ratingMA = ratingMA + calcRatingMA(SMA10.iloc[-1], close.iloc[-1])
        ratingMAC = ratingMAC + 1
    if len(SMA20):
        ratingMA = ratingMA + calcRatingMA(SMA20.iloc[-1], close.iloc[-1])
        ratingMAC = ratingMAC + 1
    if len(SMA30):
        ratingMA = ratingMA + calcRatingMA(SMA30.iloc[-1], close.iloc[-1])
        ratingMAC = ratingMAC + 1
    if len(SMA50):
        ratingMA = ratingMA + calcRatingMA(SMA50.iloc[-1], close.iloc[-1])
        ratingMAC = ratingMAC + 1
    if len(SMA100):
        ratingMA = ratingMA + calcRatingMA(SMA100.iloc[-1], close.iloc[-1])
        ratingMAC = ratingMAC + 1
    if len(SMA200):
        ratingMA = ratingMA + calcRatingMA(SMA200.iloc[-1], close.iloc[-1])
        ratingMAC = ratingMAC + 1
    if len(EMA10):
        ratingMA = ratingMA + calcRatingMA(EMA10.iloc[-1], close.iloc[-1])
        ratingMAC = ratingMAC + 1
    if len(EMA20):
        ratingMA = ratingMA + calcRatingMA(EMA20.iloc[-1], close.iloc[-1])
        ratingMAC = ratingMAC + 1
    if len(EMA30):
        ratingMA = ratingMA + calcRatingMA(EMA30.iloc[-1], close.iloc[-1])
        ratingMAC = ratingMAC + 1
    if len(EMA50):
        ratingMA = ratingMA + calcRatingMA(EMA50.iloc[-1], close.iloc[-1])
        ratingMAC = ratingMAC + 1
    if len(EMA100):
        ratingMA = ratingMA + calcRatingMA(EMA100.iloc[-1], close.iloc[-1])
        ratingMAC = ratingMAC + 1
    if len(EMA200):
        ratingMA = ratingMA + calcRatingMA(EMA200.iloc[-1], close.iloc[-1])
        ratingMAC = ratingMAC + 1

    if len(HullMA9):
        ratingHullMA9 = calcRatingMA(HullMA9[-1], close.iloc[-1])
        ratingMA = ratingMA + ratingHullMA9
        ratingMAC = ratingMAC + 1

    if len(VWMA):
        ratingVWMA = calcRatingMA(VWMA.iloc[-1], close.iloc[-1])
        ratingMA = ratingMA + ratingVWMA
        ratingMAC = ratingMAC + 1

    ratingMA =ratingMA / ratingMAC 


    ratingOther = 0
    ratingOtherC = 0
    def na(x):
        try:
            z=x[-1].isnumeric()
        except:
            z=abs(x)>=0
        return z
    ratingRSI = RSI
    if ((ratingRSI.iloc[-1]>0)):# or (ratingRSI.iloc[-2]>0)):
        ratingOtherC = ratingOtherC + 1
        ratingOther = ratingOther + calcRating(ratingRSI.iloc[-1] < 30 and ratingRSI.iloc[-2] < ratingRSI.iloc[-1], ratingRSI.iloc[-1] > 70 and ratingRSI.iloc[-2] > ratingRSI.iloc[-1])

    ratingCCI = CCI

    if len(ratingCCI) >1:
        ratingOtherC = ratingOtherC + 1
        ratingOther = ratingOther + calcRating(ratingCCI.iloc[-1] < -100 and ratingCCI.iloc[-1] > ratingCCI.iloc[-2], ratingCCI.iloc[-1] > 100 and ratingCCI.iloc[-1] < ratingCCI.iloc[-2])

    if len(adxValue) >1:
        ratingOtherC = ratingOtherC + 1
        ratingOther = ratingOther + calcRating(adxValue.iloc[-1] > 20 and adxPlus.iloc[-2] < adxMinus.iloc[-2] and adxPlus.iloc[-1] > adxMinus.iloc[-1], adxValue.iloc[-1] > 20 and adxPlus.iloc[-2] > adxMinus.iloc[-2] and adxPlus.iloc[-1] < adxMinus.iloc[-1])


    if len(Mom)>1:
        ratingOtherC = ratingOtherC + 1
        ratingOther = ratingOther + calcRating(Mom.iloc[-1] > Mom.iloc[-2], Mom.iloc[-1] < Mom.iloc[-2])

    if len(macdMACD) :
        ratingOtherC = ratingOtherC + 1
        ratingOther = ratingOther + calcRating(macdMACD.iloc[-1] > signalMACD.iloc[-1], macdMACD.iloc[-1] < signalMACD.iloc[-1])


    ratingWR = 0
    if len(WR) >1:
        ratingWR = calcRating(WR.iloc[-1] < -80 and WR.iloc[-1] > WR.iloc[-2], WR.iloc[-1] > -20 and WR.iloc[-1] < WR.iloc[-2])
    if abs(ratingWR)>0:
        ratingOtherC = ratingOtherC + 1
        ratingOther = ratingOther + ratingWR
  

    ratingBBPower = 0
    if len(BearPower)or len(BullPower):
        ratingBBPower = calcRating(
         UpTrend.iloc[-1] and BearPower.iloc[-1] < 0 and BearPower.iloc[-1] > BearPower.iloc[-2],
         DownTrend.iloc[-1] and BullPower.iloc[-1] > 0 and BullPower.iloc[-1] < BullPower.iloc[-2])
    #if not na(ratingBBPower):
    ratingOtherC = ratingOtherC + 1
    ratingOther = ratingOther + ratingBBPower

    ratingUO = 0
    #if not(na(UO)):
    ratingUO = calcRating(UO.iloc[-1] > 70, UO.iloc[-1] < 30)
    #if not na(ratingUO):
    ratingOtherC = ratingOtherC + 1
    ratingOther = ratingOther + ratingUO

    ratingOther = ratingOther / ratingOtherC

    ratingTotal = 0
    ratingTotalC = 0
    if (ratingMA):
        ratingTotal = ratingTotal + ratingMA
        ratingTotalC = ratingTotalC + 1
    if (ratingOther>=0):
        ratingTotal = ratingTotal + ratingOther
        ratingTotalC = ratingTotalC + 1
    return [round(ratingTotal,2),round( ratingOther,2), round(ratingMA,2), round(ratingOtherC,2), round(ratingMAC,2)]


def calcRatingMA(ma,close):
    #print(ma,close)
    if ma==close:
        MA=0
    elif ma<close:
        MA=1
    else:
        MA=-1
    return MA
 

def calcRating(A,B):
    if A==1:
        buy=1
        z=1
    elif B==-1:
        sell=-1
        z=-1
    else:
        z=0
    return z
StrongBound = 0.5
WeakBound = 0.1
ratingSignal='total'
def getSignal(ratingTotal, ratingOther, ratingMA) :
    res = ratingTotal
    if ratingSignal == "MAs":
        res = ratingMA
    if ratingSignal == "Oscillators":
        res = ratingOther
    return res


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

timeframe=['5T','15T','30T','1h','4h','1d']

@st.cache(allow_output_mutation=True)

def scan(symbols):
        all_signals=pd.DataFrame()
        l=len(symbols)
        count=0
        for symbol in symbols:
            count+=1
           
            print(count*100/l)
            signals=pd.DataFrame()
            timef_all=[]
            ratingTotal_all=[]
            ratingOther_all=[]
            ratingMA_all=[]
            ratingOtherC_all=[]
            ratingMAC_all=[]
            symb=[]
            print(symbol)
            if symbol=='XVG/USDT':
                break
            
            #symbol='BTC/USDT'
            #signals['symbol']=symbol
        
        
            df1=pd.DataFrame(ex.fetch_ohlcv(symbol,'5m',limit=100000),columns=['date','Open','High','Low','Close','Volume'])
            
            df1['date']=pd.to_datetime(df1['date']*1000000)
            df1=df1.set_index('date')
            for tf in timeframe:
                
                symb.append(symbol)
                df1['symbol']=symbol
                #df['date']=pd.to_datetime(df['date']*1000000)
                #df=df.set_index('date')
                df=df1.groupby(['symbol']).resample(tf).mean().reset_index()
            #    if tf=='1d':
             #       df1=pd.DataFrame(ex.fetch_ohlcv(symbol,'1d'),columns=['date','Open','High','Low','Close','Volume'])
            
              #      df1['date']=pd.to_datetime(df1['date']*1000000)
               #     df1=df1.set_index('date')
                 #   df1['symbol']=symbol
                #    df=df1
              
             
                    
                
        
         
                if len(df)>0:
                    [ratingTotal, ratingOther, ratingMA, ratingOtherC, ratingMAC]=calcRatingAll(df)
                    timef_all.append(tf)
                    
                    ratingTotal_all.append(ratingTotal)
                    ratingOther_all.append(ratingOther)
                   
                    ratingMA_all.append(ratingMA)
                    ratingOtherC_all.append(ratingOtherC)
                    ratingMAC_all.append(ratingMAC)
         
  
            signals['symbol']=symb
            signals['timeframe']=timef_all  
            signals['ratingTotal']=ratingTotal_all
            signals['ratingOther']=ratingOther_all
            signals['ratingMA']=ratingMA_all
            signals['ratingOtherC']=ratingOtherC_all
            signals['ratingMAC']=ratingMAC_all
            all_signals=pd.concat([signals,all_signals])
       
                
        
        
        StrongBound = 0.5
        WeakBound = 0.1
        ratingSignal='total'
        
        tradeSignal_all=[]
        strategy_all=[]
        for i in range(len(all_signals)):
            ratingTotal=all_signals['ratingTotal'].iloc[i]
            ratingOther=all_signals['ratingOther'].iloc[i]
            ratingMA=all_signals['ratingMA'].iloc[i]
                
            tradeSignal=(getSignal(ratingTotal, ratingOther, ratingMA))
            strategy_all.append(direction_strategy(ratingTotal, ratingOther, ratingMA))
        all_signals['strategy']=strategy_all
            
        #all_signals[all_signals['strategy']=='long'].sort_values('ratingTotal')[:30]
        
        final=pd.DataFrame()
        symbs=[]
        
        signalpower=[]
        for symbol in all_signals['symbol']:
        
            try:
                   power= all_signals[(all_signals['symbol']==symbol) &( all_signals['strategy']=='long')].groupby('strategy').symbol.count().values[0]/(len(all_signals[all_signals['symbol']==symbol]))
            except:
                   power=0
            signalpower.append(power)
        
        all_signals['signalPower']=signalpower
        all_signals['SignalWeight']=signalpower*all_signals['ratingTotal']
        z=all_signals[['symbol','strategy','signalPower','SignalWeight','timeframe']].drop_duplicates()
        print(z)
        return z

s=st.selectbox('choose the symbol BTC or USDT',['BTC','USDT','test','custom'])
if s=='BTC':
    symbols=[]        
    for i in s:
        t=i.find('DOWN/' or 'UP/' or 'BULL/' or 'BEAR/')
        if(t==-1):
            symbols.append(i)
elif s=='USDT':
    symbols=[]        
    for i in u:
        t=i.find('DOWN/' or 'UP/' or 'BULL/' or 'BEAR/')
        if(t==-1):
            symbols.append(i)
elif s=='custom':
    symbols=st.text_input('Please enter the symbols you want to check in this form ','BTC/USDT')
    
else:
    symbols=['BTC/USDT','ICP/USDT']

z=scan(symbols)    
flag=st.button('rescan again')
if flag==1:
    caching.clear_cache()
    z=scan(symbols)   
    
power_filter=st.number_input('what is the signal power to filter',value=0)
power_filter=power_filter/100
direction=st.selectbox('do you want to long or short',['short','long'])
z=z[z['strategy']==direction]
f=z[abs(z['signalPower'])>power_filter].sort_values('SignalWeight',ascending=False)
#f=f[:50].drop_duplicates()
f=f.pivot(index=['symbol','signalPower'], columns='timeframe', values=['SignalWeight','strategy'])
f=f.sort_values('signalPower',ascending=False)
st.dataframe(f)
#buy,sell=calcRatingAll(ma,close)

#'''