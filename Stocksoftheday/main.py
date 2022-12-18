# 12-18-2022 Lists the fastest highest growing stocks in the past 5 days

import yfinance as yf
from pandas_datareader import data as pdr
import pandas as pd


# lists the stocks on NASDAQ
url = "ftp://ftp.nasdaqtrader.com/SymbolDirectory/nasdaqlisted.txt"
df = pd.read_csv(url, sep="|")
print(df.head())
print(df['Symbol'].head())
print(len(df["Symbol"]))

#defines function that allows us to lookup stocks
def lookup_find(df, key_row, key_col):
    try:
        return df.iloc[key_row][key_col]
    except IndexError:
        return 0

movement_list = []

for stock in df['Symbol']:
    # gets history
    thestock = yf.Ticker(stock)
    hist = thestock.history(period = '5d')

    low = float(10000)
    high = float(0)

    for day in hist.itertuples(index=True, name='Pandas'):

        if day.Low < low:
            low = day.Low
        if high < day.High:
            high = day.High

    deltapercent = 100 * (high - low)/low
    Open = lookup_find(hist, 0, "Open")

    #error handling
    if len(hist >= 5):
        Close = lookup_find(hist, 4, "Close")
    else:
        Close = open
    
    if (open == 0.0):
        deltaprice = 0.0
    else:
        deltaprice = 100.00 * (Close - Open) / Open
    
    print(stock+" "+str(deltapercent)+ " "+ str(deltaprice))
    pair = [stock, deltapercent, deltaprice]
    movement_list.append(pair)

# prints results
for entry in movement_list:
    if entry[1] > float(100):
        print(entry)