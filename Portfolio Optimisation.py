import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
from scipy.optimize import minimize

#bongkar: each stock annualised historicals and make it the same

# Function to get user input for stock tickers
def get_stock_tickers():
    tickers = input("Enter stock tickers separated by commas: ")
    return [stock.strip() + '.JK' for stock in tickers.split(',')]

# Get user input for stock tickers
tickers = get_stock_tickers()

# Set date range for data download
endDate = datetime.today()
time_horizon= int(input("Time Horizon being Analysed (years):  "))
startDate = endDate - timedelta(days=time_horizon * 365)
print("Start Date:", startDate)

# Download Adjusted Close Price
adj_close_df = pd.DataFrame()

for ticker in tickers:
    data = yf.download(ticker, start=startDate, end=endDate)
    adj_close_df[ticker] = data['Adj Close']

# Lognormal Returns
log_returns = np.log(adj_close_df / adj_close_df.shift(1))
log_returns = log_returns.dropna()  # Drop missed values

# Covariance Matrix
cov_matrix = log_returns.cov() * 252
print(cov_matrix)

# Portfolio standard deviation
def standard_deviation(weights, cov_matrix):
    variance = weights.T @ cov_matrix @ weights
    return np.sqrt(variance)

# Expected returns based on historics
def expected_return(weights, log_returns):
    return np.sum(log_returns.mean() * weights) * 252

# Sharpe ratio
def sharpe_ratio(weights, log_returns, cov_matrix, risk_free_rate):
    return (expected_return(weights, log_returns) - risk_free_rate) / standard_deviation(weights, cov_matrix)

# Risk-free rate
risk_free_rate = float(input("Enter Risk-Free Rate (ex. 0.02): "))

# Define a function to minimize (negative Sharpe ratio)
def neg_sharpe_ratio(weights, log_returns, cov_matrix, risk_free_rate):
    return -sharpe_ratio(weights, log_returns, cov_matrix, risk_free_rate)

# Set constraints and bounds
constraints = {'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1}
bounds = [(0, 0.3) for _ in range(len(tickers))]  # 0= lower bounds; 0.3= upper bound; no shorting

# Set initial weights
initial_weights = np.array([1 / len(tickers)] * len(tickers))
print("Initial Weights:", initial_weights)

# Optimize weights to maximize Sharpe ratio
optimized_results = minimize(neg_sharpe_ratio, initial_weights, args=(log_returns, cov_matrix, risk_free_rate), method='SLSQP', constraints=constraints, bounds=bounds)

optimal_weights = optimized_results.x

# Analyze the optimal portfolio
# Display analytics of the optimal portfolio
print('Optimal Weights: ')
for ticker, weight in zip(tickers, optimal_weights):
    print(f' {ticker}: {weight:.4f}')

print()

optimal_portfolio_return = expected_return(optimal_weights, log_returns)
optimal_portfolio_volatility = standard_deviation(optimal_weights, cov_matrix)
optimal_sharpe_ratio = sharpe_ratio(optimal_weights, log_returns, cov_matrix, risk_free_rate)

print(f' Expected Annual Return: {optimal_portfolio_return:.4f}')
print(f' Expected Volatility: {optimal_portfolio_volatility:.4f}')
print(f' Sharpe Ratio: {optimal_sharpe_ratio:.4f}')