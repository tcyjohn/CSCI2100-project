#!/usr/bin/env python
from urllib.request import urlopen
import json
import certifi
import pandas as pd
import random
import os

API_KEY='iQnndIohoYBXje3aDcElMo7opczm6Ytd'

# List of stock tickers to analyze
tickers = [
    'AAPL', 'MSFT', 'NVDA', 'GOOG', 'AMZN', 'META', 'LLY', 'TSLA', 'WMT', 'JPM',
    'V', 'UNH', 'XOM', 'MA', 'PG', 'JNJ', 'ORCL', 'COST', 'HD', 'ABBV', 'KO', 'BAC',
    'MRK', 'NFLX', 'CVX', 'ADBE', 'PEP', 'TMO', 'CRM', 'LIN'
]

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

# Function to fetch and parse JSON data from a given URL
def get_jsonparsed_data(url):
    try:
        response = urlopen(url, cafile=certifi.where())
        data = response.read().decode("utf-8")
        return json.loads(data)  # Return parsed JSON data
    except Exception as e:
        print('error')  # Print error message if fetching fails

# Initialize dictionaries to store market capitalization and historical data
marketcap = {}
filtered_5_year_data = {}

# Loop through each stock ticker to retrieve data
for ticker in tickers:
    company_historical_data = []

    # Fetch market capitalization data
    url = f"https://financialmodelingprep.com/api/v3/market-capitalization/{ticker}?apikey={API_KEY}"
    marketcap[ticker] = get_jsonparsed_data(url)[0]['marketCap']  # Store market cap

    # Define desired fields for historical price data
    desiredfield = ['date', 'open', 'low', 'high', 'close', 'adjClose', 'volume']
    url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{ticker}?apikey={API_KEY}"
    
    # Fetch historical price data
    templist = get_jsonparsed_data(url)['historical']
    
    # Extract relevant fields from the historical data
    for dailydata in templist:
        tempdict = {key: dailydata[key] for key in desiredfield} 
        company_historical_data.append(tempdict)  

    # Store filtered historical data for the ticker
    filtered_5_year_data[ticker] = company_historical_data

# Part 2: Output the results to CSV files
output_dir = 'output'  # Define output directory
os.makedirs(output_dir, exist_ok=True)  # Create directory if it doesn't exist

# Create DataFrame for market capitalization and save to CSV
marketcap_df = pd.DataFrame(list(marketcap.items()), columns=['ticker', 'market_cap'])
marketcap_df['pointer'] = range(len(tickers))  # Add a pointer index column
marketcap_df.to_csv(os.path.join(output_dir, 'table1.csv'), index=False) 

# Create DataFrame for historical data and save to CSV
historical_df = pd.DataFrame(list(filtered_5_year_data.items()), columns=['ticker', 'data'])
historical_df.insert(0, 'id', range(len(tickers)))  
historical_df.to_csv(os.path.join(output_dir, 'table2.csv'), index=False)  

# Part 3: Implementing a custom Quicksort algorithm
def quicksort(S: list): 
    if len(S) <= 1:  # Base case
        return S
    Llist, Rlist = [], [] 
    pivot_pos = random.randint(0, len(S) - 1)  # Select a random pivot
    pivot = S[pivot_pos]  
    for thing in S:  
        if thing < pivot:
            Llist.append(thing)  
        elif thing > pivot:
            Rlist.append(thing)  
    # Recursively sort and combine the lists
    return quicksort(Llist) + [pivot] + quicksort(Rlist)

# Sort in alphabetical order
tickerlist = quicksort(marketcap_df['ticker'].tolist())
marketcap_df['ticker'] = pd.Categorical(marketcap_df['ticker'], categories=tickerlist, ordered=True)  
marketcapdf_sorted = marketcap_df.sort_values('ticker')  # Sort by ticker
marketcapdf_sorted.to_csv(os.path.join(output_dir, 'table1_sorted_a.csv'), index=False)  

# Sort according to market capitalizations 
marketcaplist = quicksort(marketcap_df['market_cap'].tolist())
marketcap_df['market_cap'] = pd.Categorical(marketcap_df['market_cap'], categories=marketcaplist, ordered=True) 
marketcapdf_sorted = marketcap_df.sort_values('market_cap')  # Sort by market cap
marketcapdf_sorted.to_csv(os.path.join(output_dir, 'table1_sorted_b.csv'), index=False)  