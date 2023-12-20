import json
import openai
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import yfinance as yf 


openai.api_key = open("API_KEY", "r").read()


def get_stocks(ticker):
    
    return str(yf.Ticker(ticker).history(period='1y').iloc[-1].Close)


def SMA_calculate(ticker, window):
    data = yf.Ticker(ticker).history(period='1y').Close
    
    return str(data.rolling(window=window).mean().iloc[-1])    

def EMA_calculate(ticker, window):
    data = yf.Ticker(ticker).history(period='1y').Close
    
    return str(data.ewm(span=window, adjust=False).mean().iloc[-1])

def RSI_calculate(ticker):
    data = yf.Ticker(ticker).history(period='1y').Close
    
    delta = data.diff()
    up = delta.clip(lower=0)
    down = -1 * delta.clip(upper=0)
    ema_up = up.ewm(com=14-1, adjust=False).mean()
    ema_down = down.ewm(com=14 - 1, adjust=False).mean()

    rs = ema_up / ema_down
    
    return str(100 - (100 / (1+rs)).iloc[-1])


def calculate_MACD(ticker):
    data = yf.Ticker(ticker).history(period='1y').Close
    
    short_EMA = data.ewm(span=12, adjust=False).mean()
    long_EMA = data.ewm(span=26, adjust=False).mean()
    
    MACD = short_EMA - long_EMA
    
    signal = MACD.ewm(span=9, adjust=False).mean()
    
    MACD_histogram = MACD - signal
    
    return f'{MACD[-1]}, {signal[-1]}, {MACD_histogram[-1]}'

def plot_stock(ticker):
    data = yf.Ticker(ticker).history(period='1y')
    plt.figure(figsize=(10,5))
    plt.plot(data.index, data.Close)
    plt.title('{ticker} Stock Price Over Last Year')
    plt.xlabel('Date')
    plt.ylabel('Stock Price ($)')
    
    plt.grid(True)
    plt.savefig('stock.png')
    plt.close()

    


    