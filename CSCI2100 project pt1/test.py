#!/usr/bin/env python
from dotenv import load_dotenv
import json
import os
import certifi
import pandas as pd
import random
load_dotenv()

import os
print("Current working directory:", os.getcwd())

try:
    API_KEY = os.getenv("API_KEY")
    tickers = os.getenv('TICKERS').split(',')
except Exception:
    print('error: cannot get API')

# 加载本地数据
def load_local_data():
    try:
        marketcap_df = pd.read_csv(r'C:\Users\johntsoi\Desktop\CSCI2100 project\marketcap.csv')
        historical_data_df = pd.read_csv(r'C:\Users\johntsoi\Desktop\CSCI2100 project\historical_data.csv')
        return marketcap_df, historical_data_df
    except Exception as e:
        print('Error loading local data:', e)
        return None, None
    
# 尝试加载本地数据
marketcap_df, historical_data_df = load_local_data()

if marketcap_df is not None and historical_data_df is not None:
    print("Loaded local data:")
    
else:
    print("Local data not found, fetching from API...")

def quicksort(S:list): 
    if(len(S)<=1):
        return S
    Llist,Rlist=[],[]
    pivot_pos=random.randint(0,len(S)-1)
    pivot=S[pivot_pos]
    for thing in S:
        if thing<pivot:
            Llist.append(thing)
        elif thing>pivot:
            Rlist.append(thing)
    return quicksort(Llist)+[pivot]+quicksort(Rlist)
    


tickerlist=quicksort(marketcap_df['Ticker'].tolist())
marketcap_df['Ticker'] = pd.Categorical(marketcap_df['Ticker'], categories=tickerlist, ordered=True)
marketcapdf_sorted = marketcap_df.sort_values('Ticker')
marketcapdf_sorted.to_csv('marketcap_lexi_sorted.csv',index=False)

marketcaplist=quicksort(marketcap_df['MarketCap'].tolist())
marketcap_df['MarketCap'] = pd.Categorical(marketcap_df['MarketCap'], categories=marketcaplist, ordered=True)
marketcapdf_sorted = marketcap_df.sort_values('MarketCap')
marketcapdf_sorted.to_csv('marketcap_sorted.csv',index=False)
