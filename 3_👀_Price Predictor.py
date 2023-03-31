#importing libraries

import numpy as np
import matplotlib.pyplot as plt; plt.rcdefaults()
import pandas as pd
import seaborn as sns
import math
plt.style.use('bmh')
import warnings
warnings.filterwarnings("ignore")

# fix_yahoo_finance is used to fetch data 
import yfinance as yf
yf.pdr_override()

from sklearn.linear_model import LinearRegression #for LR

#for stock news
from urllib.request import urlopen,Request
from bs4 import BeautifulSoup
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

#for lstm
import tensorflow as tf
from tensorflow.keras.layers import Dense, LSTM
from tensorflow.keras.models import Sequential
from sklearn.preprocessing import MinMaxScaler
pd.options.mode.chained_assignment = None
tf.random.set_seed(0)

#for twitter sentiment
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import unicodedata
import matplotlib.pyplot as mlpt
import got
from requests_oauthlib import OAuth1Session
import datetime

#data computatn and twitter fetch libraries 
import tweepy
import csv
import random
from textblob import TextBlob
import time
import os
import streamlit as st

from matplotlib import dates as mdates

import datetime as dt

from ta.momentum import RSIIndicator

from ta.volume import OnBalanceVolumeIndicator

import warnings
warnings.filterwarnings('ignore')

st.title('Price Predictor')

symbol = 'AAPL'

start = '2018-01-01'

end = '2023-04-01'

user_input = st.text_input('Enter Stock Ticker', 'AAPL')

dataset = yf.download(user_input, start, end)

dataset

df1 = dataset.reset_index()
X1_train = df1[df1.columns[1:5]] # data_aal[['open', 'high', 'low', 'close']]
Y1_train = df1['Adj Close']
X1_train = X1_train.values[:-1]
Y1_train = Y1_train.values[1:]
lr = LinearRegression()
lr.fit(X1_train, Y1_train)
X1_test = df1[df1.columns[1:5]].values[:-1]
Y1_test = df1['Adj Close'].values[1:]
#opening_price = float(input('Open: '))
#high = float(input('High: '))
#low = float(input('Low: '))
#close = float(input('Close: '))

st.write('Enter the following data to make a prediction:')

# Input widgets for the Open, High, Low, and Close values
open_val = st.number_input('Open Value', step=0.01)
high_val = st.number_input('High Value', step=0.01)
low_val = st.number_input('Low Value', step=0.01)
close_val = st.number_input('Close Value', step=0.01)

# Make a prediction using the LSTM model
predicted_price =  lr.predict([[open_val, high_val, low_val, close_val]])[0]
#print('Our Prediction for the opening price will be:', lr.predict([[opening_price, high, low, close]])[0])

# Display the predicted stock price
st.write(f'Predicted Stock Price: Rs. {predicted_price:.2f}')