# -*- coding: utf-8 -*-
"""
Created on Mon Jun 28 13:16:52 2021

@author: mraslan
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Jun 23 15:06:38 2021

@author: mraslan
"""
import ccxt
from schedule_manager import ScheduleManager
import streamlit as st
import pandas as pd
from crypto_signals import *
from schedule_manager import ScheduleManager
from datetime import datetime
import time
import pymongo
import pandas as pd
from streamlit import caching
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
    
flag=st.selectbox('choose the symbol BTC or USDT',['USDT','BTC'])
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
        symbo.append(i)
symbols=[]

for i in range(0,len(symbo)):
    #if symbols[i] not in a:
        symbo[i]=symbo[i].replace('/','')
a=['PAXUSDT','TUSDUSDT','USDCUSDT','BUSDUSDT','PAXGUSDT','EURUSDT','SUSDUSDT','GBPUSDT']
for symbol in symbo:
    if symbol not in a:
        symbols.append(symbol)

client = pymongo.MongoClient("mongodb://Mohamed:M12345678@cluster0-shard-00-00.otw9p.mongodb.net:27017,cluster0-shard-00-01.otw9p.mongodb.net:27017,cluster0-shard-00-02.otw9p.mongodb.net:27017/crypto_OHLCV?ssl=true&replicaSet=atlas-10tsd5-shard-0&authSource=admin&retryWrites=true&w=majority")
db = client.test
db = client["Signal_OHLCV"]
manager = ScheduleManager()
def job15m():
    print('15m')
    signal(symbols,['15m'],db)
def job1h():
    print('1h')
    signal(symbols,['1h'],db)
def job4h():
    print('4h')
    signal(symbols,['4h'],db)
def job1d():
    print('1d')
    signal(symbols,['1d'],db)


# Schedule a periodic task: do job every 60 seconds

def update_db():
    manager.register_task(name="task1", job=job15m).period(900).start_at("10:00:00").start()
    manager.register_task(name="task2", job=job1h).period(3600).start_at("10:00:00").start()
    manager.register_task(name="task3", job=job4h).period(14400).start_at("12:00:00").start()
    manager.register_task(name="task4", job=job1d).period_day_at("10:00:00").start()

@st.cache(allow_output_mutation=True)
def Call_db():
    final,times=Call_db_signals()
    return final,times


final,times =Call_db()
update_db()
#flag=st.button('Update')
#if flag==1:
#    caching.clear_cache()
 #   final,times =Call_db()
@st.cache(allow_output_mutation=True)
def get_mutable():
    return final

mutable_object = get_mutable()
if st.button('Update'):
    mutable_object=[] 
    final,times =Call_db()
flag=st.button('DB_reload')
if flag==1:
    caching.clear_cache()
    final,times =Call_db()
    update_db()

st.dataframe(final.drop_duplicates())
st.write('15m last updated at '+times[0])
st.write('1h last updated at '+times[1])
st.write('4h last updated at '+times[2])
st.write('1d last updated at '+times[3])
