import data_processing as dp
processing = dp.DataProcessing([])
import pandas as pd 
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
from scipy import stats 
from statsmodels.tsa.stattools import coint
from hurst import random_walk, compute_Hc
from numpy import log, cumsum
from numpy.random import randn
import twelvedata
import twelve_data
from alpha_vantage.timeseries import TimeSeries
import random


def twelve_data_prices(ticker, outputsize):
    ts = twelve_data.time_series_data(ticker, outputsize)
    ts = ts['close']
    #ts.fillna(0, inplace=True)
    return ts

api_key = '0Y7L7U4SDA8BGGLT'

# make the timestamp as index of the dataframe
# the files uploaded to the text file are not saved
def get_daily_returns(ticker, outputsize=5000):
    try:
        data = twelve_data_prices(ticker, outputsize)
        processing = dp.DataProcessing(data)
        data_with_dates = log(pd.DataFrame(data))
        stock_retruns = np.diff(data_with_dates['close'])
        returns = pd.DataFrame(stock_retruns)
        return returns, data
    except twelvedata.exceptions.BadRequestError as twbdr :
        # if the stock is not offered by twelve data try with alpha vantage
        print(twbdr, ticker)
        processing = dp.DataProcessing([])
        processing.to_dataframe_text(ticker)
        try:
            ts = TimeSeries(key='0Y7L7U4SDA8BGGLT', output_format='pandas')
            data, metadata = ts.get_intraday(ticker, interval='1min', outputsize='full')
            data_price = data['4. close']
            data_price.fillna(0, inplace=True)
            data_price = log(pd.DataFrame(data_price))
            stock_retruns = np.diff(data_price['4. close'])
            returns = pd.DataFrame(stock_retruns)
            return returns
        except ValueError as verr: 
            # if you ran out of API calls or the stock is not offered by alphavantage make fake one
            processing = dp.DataProcessing([])
            processing.to_dataframe_text(ticker)

            print(verr)
            data = []
            [data.append(i) for i in range(5000)]
            processing.count_down(30)
            return data
            
    except twelvedata.exceptions.TwelveDataError:
            # if you ran out of API calls use alphavantage
        try:
            ts = TimeSeries(key='0Y7L7U4SDA8BGGLT', output_format='pandas')
            data, metadata = ts.get_intraday(ticker, interval='1min', outputsize='full')
            data_price = data['4. close']
            data_price.fillna(0, inplace=True)
            data_price = log(pd.DataFrame(data_price))
            stock_retruns = np.diff(data_price['4. close'])
            returns = pd.DataFrame(stock_retruns)
            return returns
        except ValueError as verr: 
            # if you ran out of API calls or the stock is not offered by alphavantage make fake one
            processing = dp.DataProcessing([])
            processing.to_dataframe_text(ticker)
            print(verr)
            data = []
            [data.append(i) for i in range(5000)]
            processing.count_down(30)
            return data

def get_daily_prices(ticker, outputsize=5000):
    try:
        data = twelve_data_prices(ticker, outputsize)
        data = pd.DataFrame(data)
        return data
    except twelvedata.exceptions.BadRequestError:
        # if the stock is not offered by twelve data try with alpha vantage
        processing = dp.DataProcessing([])
        processing.to_dataframe_text(ticker)
        try:
            ts = TimeSeries(key='0Y7L7U4SDA8BGGLT', output_format='pandas')
            data, metadata = ts.get_intraday(ticker, interval='1min', outputsize='full')
            data_price = data['4. close']
            #data_price.fillna(0, inplace=True)
            return data_price
        except ValueError as verr: 
            # if you ran out of API calls or the stock is not offered by alphavantage make fake one
            processing = dp.DataProcessing([])
            processing.to_dataframe_text(ticker)
            print(verr)
            data = []
            [data.append(i) for i in range(5000)]
            processing.count_down(30)
            return data
            
    except twelvedata.exceptions.TwelveDataError:
            # if you ran out of API calls use alphavantage
        try:
            ts = TimeSeries(key='0Y7L7U4SDA8BGGLT', output_format='pandas')
            data, metadata = ts.get_intraday(ticker, interval='1min', outputsize='full')
            data_price = data['4. close']
            #data_price.fillna(0, inplace=True)
            return data_price
        except ValueError as verr: 
            # if you ran out of API calls or the stock is not offered by alphavantage make fake one
            processing = dp.DataProcessing([])
            processing.to_dataframe_text(ticker)
            print(verr)
            data = []
            [data.append(i) for i in range(5000)]
            processing.count_down(30)
            return data

def autocorrelation_model(datapoints, probability):
    x = [0]
    for i in range(datapoints):
        x.append(np.random.normal(0,1) + x[-1]*probability)
    plt.plot(np.cumsum(x))
    plt.show()
    return np.cumsum(x)

def normality_test(returns):
    result = stats.normaltest(returns)
    if result[1] < 0.05:
        passed = True
    else:
        passed = False
    sns.distplot(returns[0])
    plt.show()
    return passed

def check_for_synthetic_cointegrated_pairs():
    cointegrated_pairs = []
    while len(cointegrated_pairs) < 5:
        nnoise = np.random.normal(0,1,100)
        input = []
        _none = [input.append(i) for i in range(100)]
        stock1  = np.cumsum(nnoise)
        nnoise = np.random.normal(0,1,100)
        input = []
        _none = [input.append(i) for i in range(100)]
        stock2  = np.cumsum(nnoise)
        result = coint(stock1, stock2)
        if result[1] < 0.05:
            cointegrated_pairs.append((stock1,stock2))
        else:
            pass
    return cointegrated_pairs

#stocks have a probability of around 0.5
def generate_geometric_brownian_motion(probability):
    brownian = random_walk(1000, proba=probability)
    brownian = pd.DataFrame(brownian)
    brownian.plot()
    plt.show()

def check_for_synthetic_cointegrated_pairs():
    cointegrated_pairs = []
    while len(cointegrated_pairs) < 5:
        nnoise = np.random.normal(0,1,100)
        input = []
        _none = [input.append(i) for i in range(100)]
        stock1  = np.cumsum(nnoise)
        nnoise = np.random.normal(0,1,100)
        input = []
        _none = [input.append(i) for i in range(100)]
        stock2  = np.cumsum(nnoise)
        result = coint(stock1, stock2)
        if result[1] < 0.05:
            cointegrated_pairs.append((stock1,stock2))
        else:
            pass
    return cointegrated_pairs

def compare_time_series_of_I0(ts,ticker):
    # Create a Gometric Brownian Motion, Mean-Reverting and Trending Series
    gbm = log(cumsum(randn(100000))+1000)
    mr = log(randn(100000)+1000)
    tr = log(cumsum(randn(100000)+1)+1000)

    # Output the compute_Hc Exponent for each of the above series
    # and the price of ticker (the Adjusted Close price) for 
    # the ADF test given above in the article
    print("compute_Hc(GBM):   {}".format(compute_Hc(gbm)[0])) 
    print("compute_Hc(MR):    {}".format(compute_Hc(mr)[0])) 
    print("compute_Hc(TR):    {}".format(compute_Hc(tr)[0])) 

    # Assuming you have run the above code to obtain 'Ticker'!
    print(f"compute_Hc({ticker}):  {compute_Hc(ts)[0]}")
    return compute_Hc(ts)[0]

def get_random_tickers(filename, number_of_stocks):
    df = pd.read_csv(filename)
    columns = df.columns
    clean_columns = []
    for column in columns:
        if column.startswith('Unnamed'):
            pass
        else:
            clean_columns.append(column)
    df = df[clean_columns]
    print('from the collection',df)
    random_dataset = df.sample(n=number_of_stocks,axis='rows')
    return random_dataset['0']

