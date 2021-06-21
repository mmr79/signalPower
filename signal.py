# -*- coding: utf-8 -*-
"""
Created on Sun Jun 20 22:09:50 2021

@author: mraslan
"""

import ccxt
import pandas as pd
import streamlit as st
from streamlit import caching
        
from tradingview_ta import TA_Handler, Interval, Exchange
import time
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
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


@st.cache(allow_output_mutation=True)
def scan_signal(symbols):
        start_time = time.time()
        intervals=[Interval.INTERVAL_5_MINUTES ,Interval.INTERVAL_15_MINUTES,Interval.INTERVAL_1_HOUR,Interval.INTERVAL_4_HOURS ,Interval.INTERVAL_1_DAY]
        #buy=[]
        #sell=[]
        #neutral=[]
        recommendation=[]
        interv=[]
        symb=[]
        total_score=[]
        symb_score=[]
        score_indicator=[]
        tf_all=[]
        df=pd.DataFrame()
        #symbols=['BTCUSDT','ETHUSDT','ICPUSDT','XRPUSDT']
        for symbol in symbols:
            symb_rec=[]
            buyTF=' '
            score=0
            ind_score=0
            try:
                for interval in intervals:
        
                    coin = TA_Handler(
                        symbol=symbol,
                        screener="crypto",
                        exchange="binance",
                        interval=interval
                    )
                    #print(symbol,interval)
        
                    interv.append(interval)
                    symb.append(symbol)
                    x=coin.get_analysis().summary
                    #buy.append(x['BUY'])
                    #sell.append(x['SELL'])
                    ind_score=ind_score+(x['BUY']-x['SELL'])
                    #neutral.append(x['NEUTRAL'])
                    recommendation.append(x['RECOMMENDATION'])
                    symb_rec.append(x['RECOMMENDATION'])
                    if x['RECOMMENDATION']=='BUY':
                        score=score+1
                        buyTF=buyTF+' '+interval
                    elif x['RECOMMENDATION']=='STRONG_BUY':
                        score=score+2
                        buyTF=buyTF+' '+interval
                    elif x['RECOMMENDATION']=='SELL':
                        score=score-1
                    elif x['RECOMMENDATION']=='STRONG_SELL':
                        score=score-2
                    else:
                        score=score
                print(symbol,score)
                print("--- %s seconds ---" % (time.time() - start_time))
                total_score.append(score)
                symb_score.append(symbol)
                score_indicator.append(ind_score)
                tf_all.append(buyTF)
                #print(symb_score,tf_all,score_indicator)
            except:
                continue
                
        df['symbol']=symb_score
        df['Score']=total_score
        df['buy_sell_score']=score_indicator
        df['tf_buy']=tf_all
        #df['symbol']=symb
        #df['interval']=interv
        #df['buy']=buy
        #df['sell']=sell
        #df['neutral']=neutral
        #df['recommendation']=recommendation
        # Example 
        print("--- %s seconds ---" % (time.time() - start_time))
        return df
    
flag=st.selectbox('choose the symbol BTC or USDT',['BTC','USDT'])
if flag=='BTC':
    z=s
    
elif flag=='USDT':
    z=u


symbo=[]   
for i in z:
    if "DOWN/" in i or 'UP/' in i or 'BULL/' in i or 'BEAR/' in i:
        t=1
       
    else:
        t=-1
    
    
    #t=((i.find('DOWN/')) or (i.find('UP/')) or (i.find('BULL/')) or (i.find('BEAR/')))
    #print(t)
   # if(t==-1):
        #print(i)
        symbo.append(i)
symbols=[]

for i in range(0,len(symbo)):
    #if symbols[i] not in a:
        symbo[i]=symbo[i].replace('/','')
a=['PAXUSDT','TUSDUSDT','USDCUSDT','BUSDUSDT','PAXGUSDT','EURUSDT','SUSDUSDT','GBPUSDT']
for symbol in symbo:
    if symbol not in a:
        symbols.append(symbol)
        
#symbols=['PAXUSDT','TUSDUSDT','USDCUSDT','BUSDUSDT','PAXGUSDT','EURUSDT','SUSDUSDT','GBPUSDT']
#df=scan_signal(symbols)
button=st.button('rescan again')
if button==1:
    caching.clear_cache()
    df=scan_signal(symbols)  
f=df.sort_values('Score',ascending=False)[:50]
st.dataframe(f)