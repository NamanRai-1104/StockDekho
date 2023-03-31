import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import warnings
warnings.filterwarnings("ignore")
st.set_option('deprecation.showPyplotGlobalUse', False)

st.title('News Sentiment Forecast')

# Get user input for stock ticker
user_input = st.text_input('Enter a stock symbol (e.g. AAPL)', 'AAPL', key='symbol-input4')

# Set up URL and scrape news articles for stock
finviz_url='https://finviz.com/quote.ashx?t='
tickers=[user_input]
news_tables={}
for ticker in tickers:
    url = finviz_url + ticker
    req = Request(url=url,headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'})
    response = urlopen(req)
    html = BeautifulSoup(response,'html')
    news_table=html.find(id='news-table')
    news_tables[ticker]=news_table

# Extract article headlines and dates
parsed_data=[]
for ticker,news_table in news_tables.items():
    for row in news_table.findAll('tr'):
        title=row.a.text
        date_data=row.td.text.split(' ')
        if len(date_data)==1:
            time=date_data[0]
        else:
            date=date_data[0]
            time=date_data[1]
        parsed_data.append([ticker,date,time,title])

# Create DataFrame of article headlines and dates
df2=pd.DataFrame(parsed_data,columns=['ticker','date','time','title'])
st.write(df2)

# Apply sentiment analysis to headlines and create compound score column
vader=SentimentIntensityAnalyzer()
f=lambda title: vader.polarity_scores(title)['compound']
df2['compound']=df2['title'].apply(f)

# Convert date column to datetime format
df2['date']=pd.to_datetime(df2.date).dt.date

# Group DataFrame by date and calculate mean compound score for each day
mean_df2=df2.groupby(['ticker','date']).mean()
mean_df2=mean_df2.unstack()
mean_df2=mean_df2.xs('compound',axis="columns").transpose()
st.write(mean_df2)

# Plot mean compound score for each day as a bar chart
st.write("Sentiment Analysis of News Articles for ", user_input)
mean_df2.plot(kind='bar', figsize=(12, 6))
plt.xlabel("Date")
plt.ylabel("Mean Compound Score")
st.pyplot()

# Display final sentiment analysis result
mean_df = mean_df2[user_input].mean()
if mean_df>0:
    st.write("Sentiment analysis of news articles for", user_input, "shows a positive sentiment for the stock, bullish forecast.")
else:
    st.write("Sentiment analysis of news articles for", user_input, "shows a negative sentiment for the stock, bearish forecast.")
