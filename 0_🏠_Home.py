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


st.set_page_config(
    page_title="StockDekho",
    page_icon="📈",
)

st.title("Welcome to StockDekho!👋")
st.sidebar.success("Select a page above.")




symbol = 'AAPL'

start = '2018-01-01'

end = '2023-04-01'




st.title('Stock Data and Forecasts')




user_input = st.text_input('Enter Stock Ticker', 'AAPL')

dataset = yf.download(user_input, start, end)

dataset




#describing data

st.subheader('Data from 2018 - 2023')

st.write(dataset.describe())





#visualization

st.subheader('Closing Price - Annual')

fig = plt.figure(figsize = (16,8))

plt.plot(dataset['Adj Close'])

plt.title('Closing Price Chart')

plt.xlabel('Date')

plt.ylabel('Price')

plt.grid(True)

plt.show()

st.pyplot(fig)




#monthlyreturns

monthly = dataset.asfreq('BM')

monthly['Returns'] = dataset['Adj Close'].pct_change().dropna()

monthly['Month_Name'] = monthly.index.strftime("%b")

monthly['Month_Name_Year'] = monthly.index.strftime("%b-%Y")




monthly = monthly.reset_index()

monthly['Month'] = monthly["Date"].dt.month






monthly['ReturnsPositive'] = 0 < monthly['Returns']

monthly['Date'] = pd.to_datetime(monthly['Date'])

monthly['Date'] = monthly['Date'].apply(mdates.date2num)




#describing data

#st.subheader('Monthly Data')

#st.write(monthly.head())




#visualization

st.subheader('Returns for each Month')

colors = monthly.ReturnsPositive.map({True: 'g', False: 'r'})

fig = plt.figure(figsize=(30,6))

monthly['Returns'].plot(kind='bar', color = colors)

plt.xlabel("Months")

plt.ylabel("Returns")

plt.title("Returns for Each Month " + start + ' to ' + end)

plt.xticks(monthly.index, monthly['Month_Name'])

plt.show()

st.pyplot(fig)




#ANNUAL

yearly = dataset.asfreq('BY')

yearly['Returns'] = dataset['Adj Close'].pct_change().dropna()

yearly = yearly.reset_index()

yearly['Years'] = yearly['Date'].dt.year

from matplotlib import dates as mdates

import datetime as dt




yearly['ReturnsPositive'] = 0 < yearly['Returns']

yearly['Date'] = pd.to_datetime(yearly['Date'])

yearly['Date'] = yearly['Date'].apply(mdates.date2num)

dataset['Returns'] = dataset['Adj Close'].pct_change().dropna()

yearly_returns_avg = dataset['Returns'].groupby([dataset.index.year]).mean()

yearly_returns_avg




colors = yearly.ReturnsPositive.map({True: 'g', False: 'r'})

st.subheader('Returns for each Year')

fig = plt.figure(figsize=(10,5))

plt.bar(yearly['Years'], yearly['Returns'], color=colors, align='center')

plt.plot(yearly_returns_avg, marker='o', color='b')

plt.title('Yearly Returns')

plt.xlabel('Date')

plt.ylabel('Returns')

plt.show()

st.pyplot(fig)