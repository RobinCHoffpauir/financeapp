import yfinance as yf
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
st.write("""
# Simple Stock Price App
# Type the ticker symbol you wish to research, below will produce a chart with an 8 day and 20 day simple moving average.
""")

#define the ticker symbol
tickerSymbol = st.text_input('What Stock Symbol are you looking for?')
timeframe = st.selectbox('How far back do want to go?', ('1y','1d','1mo'), help='1d- 1 day, 1mo- 1 month, 1y- 1 year')
val = st.selectbox('at what time interval would you like the data?', ('1d','15m','30m','1h','1m'), help='Minimum for 1y is 1d, 1d is 1m, 1mo is 1d')
#get data on this ticker
tickerData = yf.download(tickerSymbol,period=timeframe,interval=val)
# Open	High	Low	Close	Volume
tickerData['8 Day Simple Moving Average'] = tickerData['Close'].rolling(8).mean()
tickerData['20 Day Simple Moving Average'] = tickerData['Close'].rolling(20).mean()
tickerData['Diff'] = tickerData['Close'] - tickerData['Open']
tickerData['Signal'] = np.where(tickerData['8 Day Simple Moving Average'] > tickerData['20 Day Simple Moving Average'],1,0)
tickerData['Position'] = tickerData['Signal'].diff() #using the .diff() call to get signal points
tickerData['Buy'] = np.where(tickerData['Position'] == 1,tickerData['Close'],np.NaN) #np.where(cond.,if true, if false)
tickerData['Sell'] = np.where(tickerData['Position'] == -1, tickerData['Close'],np.NaN)
st.write('''#### This is a buy sell plot using the 8 and 20 day Simple Moving Averages''')
fig= plt.figure()
plt.plot(tickerData['Close'],color='purple', label='Closing Price',zorder=1)
plt.plot(tickerData['8 Day Simple Moving Average'], color='blue', label='8 Day SMA', zorder=1)
plt.plot(tickerData['20 Day Simple Moving Average'], color='green', label='20 day SMA', zorder=1)
plt.scatter(tickerData.index,tickerData['Sell'], color='white',label='Sell', marker='_', alpha = 1, zorder=2) # red sell
plt.scatter(tickerData.index,tickerData['Buy'], color='white',label='Buy', marker='+', alpha = 1, zorder=2) #green = buy
plt.legend()
plt.style.use('dark_background')

st.pyplot(fig)
st.write("""
## Stock Price History with 8 day Simple Moving Average and 20 day Simple Moving Average
###### When the 8 Day Simple Moving Average is crosses above the 20 Day Simple Moving Average, that is a buy/long signal.
###### Just the same when 8 Day Simple Moving Average crosses under the 20 Day Simple Moving Average, that is a sell/short signal, scroll over graph below to activate interactive data
""")

st.line_chart(tickerData[['Close','8 Day Simple Moving Average','20 Day Simple Moving Average']])
st.write("""
## High/Low Price 
#### Scroll over graph to activate interactive data.
""")
st.line_chart(tickerData[['High','Low']])
