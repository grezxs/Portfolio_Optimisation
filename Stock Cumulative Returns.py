import yfinance as yf
from pandas_datareader import data as pdr
import pandas as pd
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt


#Declaring Date Range for Our Stocks Returns
#In Python the timedelta is a class that represents a duration of time
#A timedelta object represents a duration or the difference between two dates or times
endDate= dt.datetime.now()
year= int(input("Time horizon in years: "))
startDate= endDate- dt.timedelta(days=365*year)

#Create a list of stocks that we are interested in
def get_stock_tickers():
    stocks = input("Enter stock tickers separated by commas: ")
    return [stock.strip() + '.JK' for stock in stocks.split(',')]

# Get stock tickers from user
stocks = get_stock_tickers()  # Call the function to initialize 'stocks'

#Download the stock data from Yahoo Finance
#df (dataframe) is like a table in python
df= yf.download(stocks, start=startDate, end=endDate)

# Look whats in the dataframe
#print first five rows of the dataframe
# df.head()

#Select only "Adj Close"
adj_close_prices= df['Adj Close']
print(adj_close_prices.head())

#Calculate DAILY RETURNS
log_returns= np.log(adj_close_prices/adj_close_prices.shift(1))
print(log_returns.head())

#Cumulative Returns
cumulative_log_returns= log_returns.cumsum()

#Plot the cumulative returns
cumulative_log_returns.plot(title="Cumulative Returns", figsize=(10,6))

plt.show()








