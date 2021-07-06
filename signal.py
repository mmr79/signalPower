# -*- coding: utf-8 -*-
"""
Created on Wed Jul  7 00:07:17 2021

@author: mraslan
"""


from datetime import datetime
import pandas as pd
import streamlit as st
from tradingview_ta import TA_Handler, Interval, Exchange
import time
from datetime import datetime
import ccxt
import numpy as np
from tradingview_ta import *
from streamlit import caching
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

        
@st.cache(allow_output_mutation=True)
def update():
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
    analysis_5m = get_multiple_analysis(screener="crypto", interval=Interval.INTERVAL_5_MINUTES, symbols=symbols)
    analysis_15m = get_multiple_analysis(screener="crypto", interval=Interval.INTERVAL_15_MINUTES, symbols=symbols)
    analysis_1h = get_multiple_analysis(screener="crypto", interval=Interval.INTERVAL_1_HOUR, symbols=symbols)
    analysis_4h = get_multiple_analysis(screener="crypto", interval=Interval.INTERVAL_4_HOURS, symbols=symbols)
    analysis_1d = get_multiple_analysis(screener="crypto", interval=Interval.INTERVAL_1_DAY, symbols=symbols)
    analysis_1W = get_multiple_analysis(screener="crypto", interval=Interval.INTERVAL_1_WEEK, symbols=symbols)
    analysis_1M = get_multiple_analysis(screener="crypto", interval=Interval.INTERVAL_1_MONTH, symbols=symbols)
    df=pd.DataFrame()
    recommendation=np.array([])
    interv=np.array([])
    symb=np.array([])
    total_score=np.array([])
    symb_score=np.array([])
    symbs=np.array([])
    df=pd.DataFrame()
    intervs=np.array([])
    intervs_sell=np.array([])
    intervals=['5m','15m','1h','4h','1D','1W','1M']
    score_indicator=np.array([])
    for symbol in symbols:
        symb_rec=np.array([])
        buyTF=' '
        sellTF=' '
        ind_score=0
        score=0
        tf=[analysis_5m[symbol].summary,analysis_15m[symbol].summary,analysis_1h[symbol].summary,analysis_4h[symbol].summary,analysis_1d[symbol].summary,analysis_1W[symbol].summary,analysis_1M[symbol].summary]
        i=0
        for coin in tf:
            interval=intervals[i]
            i+=1
            x=coin
            interv=np.append(interv,interval)
            #symb.append(symbol)
            symb=np.append(symb,symbol)
            ind_score=ind_score+(x['BUY']-x['SELL'])
            recommendation=np.append(recommendation,x['RECOMMENDATION'])
            symb_rec=np.append(symb_rec,x['RECOMMENDATION'])
            if x['RECOMMENDATION']=='BUY':
                score=score+1
                buyTF=buyTF+' '+interval
            elif x['RECOMMENDATION']=='STRONG_BUY':
                score=score+2
                buyTF=buyTF+' '+interval
            elif x['RECOMMENDATION']=='SELL':
                score=score-1
                sellTF=sellTF+' '+interval
            elif x['RECOMMENDATION']=='STRONG_SELL':
                score=score-2
                sellTF=sellTF+' '+interval
            else:
                score=score
           
        symbs=np.append(symbs,symbol)         
        total_score=np.append(total_score,score)
        symb_score=np.append(symb_score,ind_score)
        score_indicator=np.append(score_indicator,ind_score)
        intervs=np.append(intervs,buyTF)
        intervs_sell=np.append(intervs_sell,sellTF)
    
            #print(symbol,score)
    df['symbol']=symbs
    df['Score']=total_score
    df['buy_interval']=intervs
    df['sell_intervals']=intervs_sell
    df['score_indicator']=score_indicator        
    return df

final=update()
flag=st.button('rescan again')
if flag==1:
        caching.clear_cache()
        final=update()
options = st.multiselect('What Buy Time frame you want',['5m','15m', '1h', '4h', '1d','1W','1M'],['15m','1h'])
opt=''
if '5m' in options:
    opt=opt+' 5m'
if '15m' in options:
    opt=opt+' 15m'
if '1h' in options:
    opt=opt+' 1h'
if '4h' in options:
    opt=opt+' 4h'
if '1d' in options:
    opt=opt+' 1d'
if '1W' in options:
    opt=opt+' 1W'
if '1M' in options:
    opt=opt+' 1M'


opt=opt.replace(" ","")


final['buy_interval'] = final['buy_interval'].str.replace(" ","")
if len(opt)>0:
    f=final[final['buy_interval']==opt]
else:
    f=final
st.dataframe(f.sort_values('Score',ascending=False).drop_duplicates())

symbol=st.selectbox('Symbol',final.symbol)
st.dataframe(final[final['symbol']==symbol].sort_values('Score',ascending=False).drop_duplicates())

