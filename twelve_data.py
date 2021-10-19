import pandas as pd
import numpy as np
import requests
from twelvedata import TDClient
import matplotlib.pyplot as plt
import matplotlib.image as mpllimg

cvs_documentation = 'https://pythonexamples.org/python-opencv-cv2-imwrite-save-image/#:~:text=To%20save%20image%20to%20local%20storage%20using%20Python%2C,numpy%20array.%20cv2.imwrite%20%28%29%20returns%20a%20boolean%20value.'
api_documentation_url = 'https://twelvedata.com/docs#stddev'
python_documentation = 'https://docs.python.org/3/library/functions.html#func-list'
matplotlib_docum = 'https://matplotlib.org/stable/tutorials/introductory/pyplot.html'
api_github = 'https://github.com/twelvedata/twelvedata-python#Time-series'

api_k = '2fd74f1ebfac437f9190eb9edc130f83'
#time_interval = '5min'
try:
    td = TDClient(apikey=api_k)
except requests.exceptions.ConnectionError:
    print('max number of requests exceded')
    use_alpha_vantage = True

ticker_symbol = ''
api_url1 = f"https://api.twelvedata.com/cryptocurrencies"
api_url2 = f"https://api.twelvedata.com/etf"
api_url3 = f"https://api.twelvedata.com/indices"
api_url4 = f"https://api.twelvedata.com/exchanges"
api_url5 = f"https://api.twelvedata.com/earliest_timestamp?symbol={ticker_symbol}&interval=5min&apikey={api_k}"
api_url6 = f"https://api.twelvedata.com/price?symbol=AAPL&apikey={api_k}"
api_url7 = f"https://api.twelvedata.com/forex_pairs"

def get_info(api_url1):
    f_x = requests.get(api_url1).json()
    return f_x
#data1 = []
#for x in f_x['data']:
#    data1.append(x['symbol'])
#print(f_x['price'])
#print(f_x['datetime'])

def get_real_time_data(ticker):
    responsen = requests.get(f"https://api.twelvedata.com/price?symbol={ticker}&apikey={api_k}").json()
    w2 = responsen['price']
    return w2

def time_series_data(ticker, outputsize, time_interval='1min'):
    ts = td.time_series(
        symbol=ticker,
        interval=time_interval,
        outputsize=outputsize,
        timezone="America/New_York",
    ).as_pandas()
    return ts

def time_serie(ticker, outputsize, time_interval='1min'):
    ts = td.time_series(
        symbol=ticker,
        interval=time_interval,
        outputsize=outputsize,
        timezone="America/New_York",
    )
    return ts

def candles_visualization_tool(ticker, outputsize):
    data = time_serie(ticker, outputsize, time_interval='1min').with_rsi().as_pyplot_figure()
    plt.show()


