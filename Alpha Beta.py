import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import os
import statsmodels.api as sm

# Initial string of tickers
tickers_string = """
^JKSE ABDA.JK ADMF.JK AGRO.JK AGRS.JK AHAP.JK AMAG.JK APIC.JK ARTO.JK ASBI.JK ASDM.JK ASJT.JK ASMI.JK ASRM.JK
BABP.JK BACA.JK BBCA.JK BBHI.JK BBKP.JK BBLD.JK BBMD.JK BBNI.JK BBRI.JK BBTN.JK BBYB.JK BCAP.JK BCIC.JK
BDMN.JK BEKS.JK BFIN.JK BGTG.JK BINA.JK BJBR.JK BJTM.JK BKSW.JK BMAS.JK BMRI.JK BNBA.JK BNGA.JK BNII.JK
BNLI.JK BPFI.JK BPII.JK BSIM.JK BSWD.JK BTPN.JK BVIC.JK CFIN.JK DEFI.JK DNAR.JK DNET.JK GSMF.JK HDFA.JK
INPC.JK LPGI.JK LPPS.JK MAYA.JK MCOR.JK MEGA.JK MFIN.JK MREI.JK NISP.JK NOBU.JK OCAP.JK PADI.JK PALM.JK
PANS.JK PEGE.JK PLAS.JK PNBN.JK PNBS.JK PNIN.JK PNLF.JK POOL.JK RELI.JK SDRA.JK SMMA.JK SRTG.JK STAR.JK
TIFA.JK TRIM.JK TRUS.JK VICO.JK VINS.JK VRNA.JK WOMF.JK YULE.JK CASA.JK BRIS.JK MTWI.JK JMAS.JK NICK.JK
BTPS.JK TUGU.JK POLA.JK SFAN.JK LIFE.JK FUJI.JK AMAR.JK AMOR.JK BHAT.JK BBSI.JK BANK.JK MASB.JK VTNY.JK
"""

# Split the string into a list of tickers
tickers_list = tickers_string.split()

# Set Date and Time
end_date = datetime.today()
start_date = end_date - timedelta(days=5 * 365)

# Create a DataFrame to store close prices
data_frames = []

# Download close prices for each ticker
for ticker in tickers_list:
    try:
        data = yf.download(ticker, start=start_date, end=end_date)
        if not data.empty:
            data_frames.append(data['Close'].rename(ticker))
    except Exception as e:
        print(f"Failed to download {ticker}: {e}")

# Concatenate all DataFrames into a single DataFrame
close_df = pd.concat(data_frames, axis=1)

# Calculate daily returns
returns_df = close_df.pct_change().dropna()

# Extract JKSE returns for regression
jkse_returns = returns_df['^JKSE']

# Initialize lists to store alpha and beta values
alpha_values = []
beta_values = []

# Calculate alpha and beta for each stock
for ticker in returns_df.columns:
    if ticker != '^JKSE':
        # Prepare the regression model
        X = sm.add_constant(jkse_returns)  # Add constant for intercept
        y = returns_df[ticker]

        model = sm.OLS(y, X).fit()

        # Extract alpha (intercept) and beta (slope)
        alpha = model.params[0]  # Intercept
        beta = model.params[1]  # Slope

        alpha_values.append(alpha)
        beta_values.append(beta)

# Create a DataFrame for the results
results_df = pd.DataFrame({
    'Ticker': returns_df.columns[1:],  # Exclude JKSE
    'Alpha': alpha_values,
    'Beta': beta_values
})

# Set Output Folder and Export Data
output_folder = r"/Users/gracechandra/Documents/Python for Finance_Learning"
output_file = os.path.join(output_folder, 'stock_alpha_beta.xlsx')
results_df.to_excel(output_file, index=False)

print("Alpha and Beta calculations exported successfully!")
#
# import pandas as pd
# import yfinance as yf
# from datetime import datetime, timedelta
# import os
# import statsmodels.api as sm
# import matplotlib.pyplot as plt
#
# # Initial string of tickers
# tickers_string = """
# ^JKSE ABDA.JK ADMF.JK AGRO.JK AGRS.JK AHAP.JK AMAG.JK APIC.JK ARTO.JK ASBI.JK ASDM.JK ASJT.JK ASMI.JK ASRM.JK
# BABP.JK BACA.JK BBCA.JK BBHI.JK BBKP.JK BBLD.JK BBMD.JK BBNI.JK BBRI.JK BBTN.JK BBYB.JK BCAP.JK BCIC.JK
# BDMN.JK BEKS.JK BFIN.JK BGTG.JK BINA.JK BJBR.JK BJTM.JK BKSW.JK BMAS.JK BMRI.JK BNBA.JK BNGA.JK BNII.JK
# BNLI.JK BPFI.JK BPII.JK BSIM.JK BSWD.JK BTPN.JK BVIC.JK CFIN.JK DEFI.JK DNAR.JK DNET.JK GSMF.JK HDFA.JK
# INPC.JK LPGI.JK LPPS.JK MAYA.JK MCOR.JK MEGA.JK MFIN.JK MREI.JK NISP.JK NOBU.JK OCAP.JK PADI.JK PALM.JK
# PANS.JK PEGE.JK PLAS.JK PNBN.JK PNBS.JK PNIN.JK PNLF.JK POOL.JK RELI.JK SDRA.JK SMMA.JK SRTG.JK STAR.JK
# TIFA.JK TRIM.JK TRUS.JK VICO.JK VINS.JK VRNA.JK WOMF.JK YULE.JK CASA.JK BRIS.JK MTWI.JK JMAS.JK NICK.JK
# BTPS.JK TUGU.JK POLA.JK SFAN.JK LIFE.JK FUJI.JK AMAR.JK AMOR.JK BHAT.JK BBSI.JK BANK.JK MASB.JK VTNY.JK
# """
#
# # Split the string into a list of tickers
# tickers_list = tickers_string.split()
#
# # Set Date and Time
# end_date = datetime.today()
# start_date = end_date - timedelta(days=5 * 365)
#
# # Create a DataFrame to store close prices
# data_frames = []
#
# # Download close prices for each ticker
# for ticker in tickers_list:
#     try:
#         data = yf.download(ticker, start=start_date, end=end_date)
#         if not data.empty:
#             data_frames.append(data['Close'].rename(ticker))
#     except Exception as e:
#         print(f"Failed to download {ticker}: {e}")
#
# # Concatenate all DataFrames into a single DataFrame
# close_df = pd.concat(data_frames, axis=1)
#
# # Calculate daily returns
# returns_df = close_df.pct_change().dropna()
#
# # Extract JKSE returns for regression
# jkse_returns = returns_df['^JKSE']
#
# # Initialize lists to store alpha and beta values
# alpha_values = []
# beta_values = []
#
# # Calculate alpha and beta for each stock
# for ticker in returns_df.columns:
#     if ticker != '^JKSE':
#         # Prepare the regression model
#         X = sm.add_constant(jkse_returns)  # Add constant for intercept
#         y = returns_df[ticker]
#
#         model = sm.OLS(y, X).fit()
#
#         # Extract alpha (intercept) and beta (slope)
#         alpha = model.params[0]  # Intercept
#         beta = model.params[1]  # Slope
#
#         alpha_values.append(alpha)
#         beta_values.append(beta)
#
# # Create a DataFrame for the results
# results_df = pd.DataFrame({
#     'Ticker': returns_df.columns[1:],  # Exclude JKSE
#     'Alpha': alpha_values,
#     'Beta': beta_values
# })
#
# # Create a bubble chart
# plt.figure(figsize=(12, 8))
# plt.scatter(results_df['Beta'], results_df['Alpha'], s=100, alpha=0.5, c='blue', edgecolors='w', linewidth=0.5)
#
# # Annotate each point with the ticker
# for i in range(len(results_df)):
#     plt.annotate(results_df['Ticker'][i], (results_df['Beta'][i], results_df['Alpha'][i]), fontsize=8, ha='right')
#
# # Set labels and title
# plt.title('Bubble Chart of Alpha vs Beta for Tickers')
# plt.xlabel('Beta')
# plt.ylabel('Alpha')
#
# # Show grid
# plt.grid(True)
#
# # Show the plot
# plt.show()
#
# # Set Output Folder and Export Data
# output_folder = r"/Users/gracechandra/Documents/Python for Finance_Learning"
# output_file = os.path.join(output_folder, 'stock_alpha_beta.xlsx')
# results_df.to_excel(output_file, index=False)
#
# print("Alpha and Beta calculations exported successfully!")
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import os
import statsmodels.api as sm
import matplotlib.pyplot as plt

import yfinance as yf
import pandas as pd

# # Set a custom User-Agent
# yf.pd.options.display.float_format = '{:.2f}'.format
# yf.Ticker('ASRM.JK').history(period='1d', actions=False)

# import time
# time.sleep(1)  # 1-second delay between requests

# # Initial string of tickers
# tickers_string = """
# ^JKSE ABDA.JK ADMF.JK AGRO.JK AGRS.JK AHAP.JK AMAG.JK APIC.JK ARTO.JK ASBI.JK ASDM.JK ASJT.JK ASMI.JK ASRM.JK
# BABP.JK BACA.JK BBCA.JK BBHI.JK BBKP.JK BBLD.JK BBMD.JK BBNI.JK BBRI.JK BBTN.JK BBYB.JK BCAP.JK BCIC.JK
# BDMN.JK BEKS.JK BFIN.JK BGTG.JK BINA.JK BJBR.JK BJTM.JK BKSW.JK BMAS.JK BMRI.JK BNBA.JK BNGA.JK BNII.JK
# BNLI.JK BPFI.JK BPII.JK BSIM.JK BSWD.JK BTPN.JK BVIC.JK CFIN.JK DEFI.JK DNAR.JK DNET.JK GSMF.JK HDFA.JK
# INPC.JK LPGI.JK LPPS.JK MAYA.JK MCOR.JK MEGA.JK MFIN.JK MREI.JK NISP.JK NOBU.JK OCAP.JK PADI.JK PALM.JK
# PANS.JK PEGE.JK PLAS.JK PNBN.JK PNBS.JK PNIN.JK PNLF.JK POOL.JK RELI.JK SDRA.JK SMMA.JK SRTG.JK STAR.JK
# TIFA.JK TRIM.JK TRUS.JK VICO.JK VINS.JK VRNA.JK WOMF.JK YULE.JK CASA.JK BRIS.JK MTWI.JK JMAS.JK NICK.JK
# BTPS.JK TUGU.JK POLA.JK SFAN.JK LIFE.JK FUJI.JK AMAR.JK AMOR.JK BHAT.JK BBSI.JK BANK.JK MASB.JK VTNY.JK
# """
#
# # Split the string into a list of tickers
# tickers_list = tickers_string.split()
#
# # Set Date and Time
# end_date = datetime.today()
# start_date = end_date - timedelta(days=5 * 365)
#
# # Create a DataFrame to store close prices
# data_frames = []
#
# # Initialize lists to store alpha, beta, and dividend yield values
# alpha_values = []
# beta_values = []
# dividend_yields = []
#
# # Download close prices and dividend yield for each ticker
# for ticker in tickers_list:
#     try:
#         # Download historical data
#         data = yf.download(ticker, start=start_date, end=end_date)
#         if not data.empty:
#             data_frames.append(data['Close'].rename(ticker))
#
#             # Get the dividend yield
#             stock_info = yf.Ticker(ticker)
#             dividend_yield = stock_info.info.get('dividendYield', 0)  # Default to 0 if not available
#             dividend_yields.append(dividend_yield)
#
#     except Exception as e:
#         print(f"Failed to download {ticker}: {e}")
#         dividend_yields.append(None)  # Append None if there's an error
#
# # Concatenate all DataFrames into a single DataFrame
# close_df = pd.concat(data_frames, axis=1)
#
# # Calculate daily returns
# returns_df = close_df.pct_change().dropna()
#
# # Extract JKSE returns for regression
# jkse_returns = returns_df['^JKSE']
#
# # Calculate alpha and beta for each stock
# for ticker in returns_df.columns:
#     if ticker != '^JKSE':
#         # Prepare the regression model
#         X = sm.add_constant(jkse_returns)  # Add constant for intercept
#         y = returns_df[ticker]
#
#         model = sm.OLS(y, X).fit()
#
#         # Extract alpha (intercept) and beta (slope)
#         alpha = model.params[0]  # Intercept
#         beta = model.params[1]  # Slope
#
#         alpha_values.append(alpha)
#         beta_values.append(beta)
#
# # Create a DataFrame for the results
# results_df = pd.DataFrame({
#     'Ticker': returns_df.columns[1:],  # Exclude JKSE
#     'Alpha': alpha_values,
#     'Beta': beta_values,
#     'Dividend Yield': dividend_yields  # Add dividend yield
# })
#
# # Create a bubble chart
# plt.figure(figsize=(12, 8))
# plt.scatter(results_df['Beta'], results_df['Alpha'], s=100, alpha=0.5, c='blue', edgecolors='w', linewidth=0.5)
#
# # Annotate each point with the ticker
# for i in range(len(results_df)):
#     plt.annotate(results_df['Ticker'][i], (results_df['Beta'][i], results_df['Alpha'][i]), fontsize=8, ha='right')
#
# # Set labels and title
# plt.title('Bubble Chart of Alpha vs Beta for Tickers')
# plt.xlabel('Beta')
# plt.ylabel('Alpha')
#
# # Show grid
# plt.grid(True)
#
# # Show the plot
# plt.show()
#
# # Set Output Folder and Export Data
# output_folder = r"/Users/gracechandra/Documents/Python for Finance_Learning"
# output_file = os.path.join(output_folder, 'stock_alpha_beta.xlsx')
# results_df.to_excel(output_file, index=False)
#
# print("Alpha, Beta, and Dividend Yield calculations exported successfully!")