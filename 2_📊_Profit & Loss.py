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

st.title('Profit & Loss')

start = '2018-01-01'

end = '2023-01-01'

#Profit and Loss in trading
#1. P&L for daily
st.subheader('Daily Profit & Loss')

#Get Stock data
user_input = st.text_input('Enter a stock symbol (e.g. AAPL)', 'AAPL', key='symbol-input3')
dataset1 = yf.download(user_input, start, end)
Start = 5000 # How much to invest
dataset1['Shares'] = 0
dataset1['PnL'] = 0
dataset1['End'] = Start
dataset1['Shares'] = dataset1['End'].shift(1) / dataset1['Adj Close'].shift(1)
dataset1['PnL'] = dataset1['Shares'] * (dataset1['Adj Close'] - dataset1['Adj Close'].shift(1))
dataset1['End'] = dataset1['End'].shift(1) + dataset1['PnL']

# Create a plot
fig1, ax = plt.subplots()
ax.plot(dataset1['PnL'])
ax.set_ylabel('Price')
ax.set_xlabel('Date')
ax.legend()

# Display the plot using Streamlit
st.pyplot(fig1)

#2. Profit or Loss
st.subheader('Profit or Loss')

# How many shares can get with the current money?
Shares = round(int(float(Start) / dataset1['Adj Close'][0]),1)
Purchase_Price = dataset1['Adj Close'][0] # Invest in the Beginning Price
Current_Value = dataset1['Adj Close'][-1] # Value of stock of Ending Price
Purchase_Cost = Shares * Purchase_Price
Current_Value = Shares * Current_Value
Profit_or_Loss = Current_Value - Purchase_Cost
percentage_gain_or_loss = (Profit_or_Loss/Current_Value) * 100
percentage_returns = (Current_Value - Purchase_Cost)/ Purchase_Cost 
net_gains_or_losses = (dataset1['Adj Close'][-1] - dataset1['Adj Close'][0]) / dataset1['Adj Close'][0]
total_return = ((Current_Value/Purchase_Cost)-1) * 100

# Get P&L by symbol
#df_pnl_by_symbol = dataset1.groupby('user_input').sum()['PnL']

# Display total P&L
st.write('Total P&L: ${:,.2f}'.format(Profit_or_Loss))
st.write('Percentage Gain or Loss: %s %%' % round(percentage_gain_or_loss,2))
st.write('Percentage of Returns: %s %%' % round(percentage_returns,2))
st.write('Net gains or losses: %s %%' % round(net_gains_or_losses,2))
st.write('Total Returns: %s %%' % round(total_return,2))