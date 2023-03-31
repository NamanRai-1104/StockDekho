import streamlit as st
import tweepy
import pandas as pd
from textblob import TextBlob
import re
import yfinance as yf
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# Authenticate Twitter API credentials
consumer_key = 'mYgCy1C8QPB1KTh4nAs6iaO8a'
consumer_secret = 'RTxoVtF41IeMbFPxgCmizPLrH9hQbeLsNc8e8mpL8wNlDtX52i'
access_token = '1397060523783458817-HSrlh3NABJqqYdxcAbvUE6vugnA1PP'
access_token_secret = 'RZr5V7qEgWnRRdOHVJDHsiGaATHfEWN2qCpeqNLvXGZkC'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# Define a function to clean the text
def clean_text(text):
    text = re.sub('@[A-Za-z0–9]+', '', text) # Removing mentions
    text = re.sub('#', '', text) # Removing hashtags
    text = re.sub('RT[\s]+', '', text) # Removing retweets
    text = re.sub('https?:\/\/\S+', '', text) # Removing hyperlinks
    return text

# Define a function to get sentiment score
def get_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity

# Define a function to get stock price data
def get_stock_price_data(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    return stock_data

# Define a function to plot stock price data
def plot_stock_price_data(stock_data):
    plt.plot(stock_data['Adj Close'])
    plt.xlabel('Date')
    plt.ylabel('Price ($)')
    plt.title('Stock Price')
    st.pyplot()

# Define a function to plot sentiment scores
def plot_sentiment_scores(sentiment_scores):
    plt.plot(sentiment_scores)
    plt.xlabel('Date')
    plt.ylabel('Sentiment Score')
    plt.title('Sentiment Analysis')
    st.pyplot()

# Set up Streamlit app
st.title('Twitter Sentiment Analysis')

# Get user input
ticker = st.text_input('Enter a stock ticker (e.g. AAPL):')
start_date = st.date_input('Select a start date:')
end_date = st.date_input('Select an end date:')

# Get stock price data
stock_data = get_stock_price_data(ticker, start_date, end_date)

# Plot stock price data
plot_stock_price_data(stock_data)

# Get tweets and sentiment scores
tweets = tweepy.Cursor(api.search_tweets, q=ticker, lang='en').items(100)
fetch_tweets = tweepy.Cursor(api.search_tweets, q=ticker, tweet_mode='extended', lang='en').items()
data=pd.DataFrame(data=[[tweet_info.created_at.date(),tweet_info.full_text]for tweet_info in fetch_tweets],columns=['Date','Tweets'])

sentiment_scores = []
for tweet in tweets:
    cleaned_text = clean_text(tweet.text)
    sentiment_score = get_sentiment(cleaned_text)
    sentiment_scores.append(sentiment_score)

st.write(data)

# Plot sentiment scores
plot_sentiment_scores(sentiment_scores)
