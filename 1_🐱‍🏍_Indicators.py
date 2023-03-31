import numpy as np

import matplotlib.pyplot as plt

import pandas as pd

import pandas_datareader as data

import yfinance as yf

from keras.models import load_model

import streamlit as st

import calendar

import datetime

from matplotlib import dates as mdates

import datetime as dt

from ta.momentum import RSIIndicator

from ta.volume import OnBalanceVolumeIndicator

import warnings
warnings.filterwarnings('ignore')

st.title('Indicators')

#indicators

#1. SMA EMA

# Import libraries

import talib as ta
st.subheader('SMA & EMA')
# Get stock data
symbol = st.text_input('Enter a stock symbol (e.g. AAPL)')
stock_data = yf.Ticker(symbol).history(period='max')

# Calculate moving averages
sma = stock_data['Close'].rolling(window=20).mean()
ema = stock_data['Close'].ewm(span=20, adjust=False).mean()

# Create a plot
fig, ax = plt.subplots()
ax.plot(stock_data.index, stock_data['Close'], label='Close')
ax.plot(sma.index, sma, label='SMA')
ax.plot(ema.index, ema, label='EMA')
ax.legend()

# Display the plot using Streamlit
st.pyplot(fig)


#2. Bollinger Bands
st.subheader('Bollinger Bands')

# Get stock data
stock_data = yf.Ticker(symbol).history(period='max')

# Calculate Bollinger Bands
rolling_mean = stock_data['Close'].rolling(window=20).mean()
rolling_std = stock_data['Close'].rolling(window=20).std()
upper_band = rolling_mean + 2 * rolling_std
lower_band = rolling_mean - 2 * rolling_std

# Create a plot
fig, ax = plt.subplots()
ax.plot(stock_data.index, stock_data['Close'], label='Close')
ax.plot(rolling_mean.index, rolling_mean, label='Moving Average')
ax.plot(upper_band.index, upper_band, label='Upper Band')
ax.plot(lower_band.index, lower_band, label='Lower Band')
ax.fill_between(upper_band.index, upper_band, lower_band, alpha=0.1)
ax.legend()

# Display the plot using Streamlit
st.pyplot(fig)


#3. RSI
st.subheader('RSI')
# Get stock data
stock_data = yf.Ticker(symbol).history(period='max')

# Calculate RSI
rsi = RSIIndicator(stock_data['Close'], window=14)
stock_data['RSI'] = rsi.rsi()

# Create a plot
fig, ax = plt.subplots()
ax.plot(stock_data.index, stock_data['RSI'], label='RSI')
ax.set_ylabel('RSI')
ax.set_xlabel('Date')
ax.legend()

# Display the plot using Streamlit
st.pyplot(fig)

#4. OBV
st.subheader('OBV')
# Get stock data
stock_data = yf.Ticker(symbol).history(period='max')

# Calculate OBV
obv = OnBalanceVolumeIndicator(stock_data['Close'], stock_data['Volume'])
stock_data['OBV'] = obv.on_balance_volume()

# Create a plot
fig, ax = plt.subplots()
ax.plot(stock_data.index, stock_data['OBV'], label='OBV')
ax.set_ylabel('OBV')
ax.set_xlabel('Date')
ax.legend()

# Display the plot using Streamlit
st.pyplot(fig)