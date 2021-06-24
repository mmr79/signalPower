# -*- coding: utf-8 -*-
"""
Created on Wed Jun 23 15:06:46 2021

@author: mraslan
"""

from tradingview_ta import TA_Handler, Interval, Exchange
import time
import pandas as pd
from datetime import datetime
import pymongo

def Call_db_signals():
    client = pymongo.MongoClient("mongodb://Mohamed:M12345678@cluster0-shard-00-00.otw9p.mongodb.net:27017,cluster0-shard-00-01.otw9p.mongodb.net:27017,cluster0-shard-00-02.otw9p.mongodb.net:27017/crypto_OHLCV?ssl=true&replicaSet=atlas-10tsd5-shard-0&authSource=admin&retryWrites=true&w=majority")
    db = client.test
    db = client["Signal_OHLCV"]
    times=[]
    ooo='OHLCV'+'15m'
    mycol = db[ooo]
    mydoc = mycol.find().sort("Date")
    df_15=pd.DataFrame(mydoc)
    times.append(str(df_15.Date[0]))
    df_15.drop(columns=['_id','Date'],axis=1,inplace=True)
  
    
    ooo='OHLCV'+'1h'
    mycol = db[ooo]
    mydoc = mycol.find().sort("Date")
    df_1=pd.DataFrame(mydoc)
    times.append(str(df_1.Date[0]))
    df_1.drop(columns=['_id','Date'],axis=1,inplace=True)
  
    ooo='OHLCV'+'4h'
    mycol = db[ooo]
    mydoc = mycol.find().sort("Date")
    df=pd.DataFrame(mydoc)
    times.append(str(df.Date[0]))
    df.drop(columns=['_id','Date'],axis=1,inplace=True)
    ooo='OHLCV'+'1h'
    mycol = db[ooo]
    mydoc = mycol.find().sort("Date")
    df_1=pd.DataFrame(mydoc)
    times.append(str(df_1.Date[0]))
    df_1.drop(columns=['_id','Date'],axis=1,inplace=True)
  
    ooo='OHLCV'+'1d'
    mycol = db[ooo]
    mydoc = mycol.find().sort("Date")
    df_1d=pd.DataFrame(mydoc)
    times.append(str(df_1d.Date[0]))
    df_1d.drop(columns=['_id','Date'],axis=1,inplace=True)
    
    df=df.set_index('symbol').join(df_1.set_index('symbol'), lsuffix='_4h', rsuffix='_1h')
    
    df1=df.join(df_1d.set_index('symbol'),  rsuffix='_1d')
    df=df1.join(df_15.set_index('symbol'),  rsuffix='_15m')
    final=pd.DataFrame()
    final['interval']=df['interval_4h']+' '+df['interval_1h']+' '+df['interval']+' '+df['interval_15m']
    final['Score']=df['Score_4h']+df['Score_1h']+df['Score']+df['Score_15m']
    final['Score_indicators']=df['score_indicator_4h']+df['score_indicator_1h']+df['score_indicator']+df['score_indicator_15m']
    final=final.sort_values('Score',ascending=False).dropna()
    return final,times




def signal(symbols,intervals,db):
    
    recommendation=[]
    interv=[]
    symb=[]
    total_score=[]
    symb_score=[]
    df=pd.DataFrame()
    intervs=[]
    
    score_indicator=[]
    #symbols=['BTCUSDT','ETHUSDT','ICPUSDT','XRPUSDT']
    #Date=[]
    for symbol in symbols:
        symb_rec=[]
        buyTF=' '
        ind_score=0
        score=0
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
                #neutral.append(x['NEUTRAL'])
                ind_score=ind_score+(x['BUY']-x['SELL'])
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
            #print("--- %s seconds ---" % (time.time() - start_time))
            total_score.append(score)
            symb_score.append(symbol)
            score_indicator.append(ind_score)
            intervs.append(buyTF)
            #Date.append(Dates)
        except:
            continue

    df['symbol']=symb_score
    df['Score']=total_score
    df['interval']=intervs
    df['score_indicator']=score_indicator
    df['Date']=datetime.now()
    #df['symbol']=symb
    #df['interval']=interv
    #df['buy']=buy
    #df['sell']=sell
    #df['neutral']=neutral
    #df['recommendation']=recommendation
    # Example 
    ooo='OHLCV'+interval
    mycol = db[ooo]
    mycol.drop()
    mycol = db[ooo]
    data = df.to_dict(orient='records')  # Here's our added param..
    mycol.insert_many(data)
    print(ooo)
   # print("--- %s seconds ---" % (time.time() - start_time))