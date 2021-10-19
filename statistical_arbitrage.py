import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller, coint
import pandas as pd
import data_processing as dtp
_data = dtp.DataProcessing([])
import os
from os import path as ps
ROOT_DIR = os.path.dirname(os.getcwd())
from check_for_returns import compare_time_series_of_I0, get_daily_returns
import numpy as np
from matplotlib import pyplot as plt


def check_for_stationarity(collection_of_tickers, cutoff=0.01):
    stationary_stocks = []
    for ticker in collection_of_tickers:
        x = get_daily_returns(ticker)
        passed = False
        try:
            pvalue = adfuller(x[0])[1]
            if pvalue < cutoff:
                print('p-value = ' + str(pvalue) + 'The series ' + ticker +' is likely to be stationary')
                passed =  True
            else:
                print('p-value = ' + str(pvalue) + 'The series ' + ticker +' is likely to be non_stationary')
                passed = False
        except ValueError:
            pass
        if passed:
            stationary_stocks.append(ticker)
        else:
            pass
    return stationary_stocks

def Hurst_exponent_comparison_test(collection_of_tickets):
    stationary_stocks = []
    passed = False
    for ticker in collection_of_tickets:
        ts = get_daily_returns(ticker)
        try:
            tx = compare_time_series_of_I0(ts[0],ticker)
        except ValueError:
            tx = 10
        except TypeError:
            tx = 10
        if tx < 0.5:
            passed = True
        else:
            passed = False
        if passed:
            stationary_stocks.append((ticker,ts))
        else:
            pass
    return stationary_stocks

def construct_synthetic_price(ticker_symbol1, ticker_symbol2):
    data = pd.read_csv(r'data for trading\stationary stocks returns.csv')
    try:
        x1 = data[ticker_symbol1]
        x2 = data[ticker_symbol2]
        if x1.mean() > x2.mean():   
            x2 = sm.add_constant(x2)
            results = sm.OLS(np.array(x1),np.array(x2)).fit()
            b = results.params[0]
            x1 = pd.DataFrame(x1)
            x2 = x2['const'] + x2[ticker_symbol2]
            spread = x1[ticker_symbol1] - b*x2
        else:
            x1 = sm.add_constant(x1)
            results = sm.OLS(np.array(x2),np.array(x1)).fit()
            b = results.params[0]
            x2 = pd.DataFrame(x2)
            x1 = x1['const'] + x1[ticker_symbol1]
            spread = x2[ticker_symbol2] - b*x1
    except KeyError:
        x1 = get_daily_returns(ticker_symbol1)[0]
        x2 = get_daily_returns(ticker_symbol2)[0]

        try:
            if x1.mean()[0] > x2.mean()[0]:   
                x2 = sm.add_constant(x2)
                results = sm.OLS(np.array(x1),np.array(x2)).fit()# be careful for diffferent siizes ValueError:
                b = results.params[0]
                x1 = pd.DataFrame(x1)
                x2 = x2['const'] + x2[0]
                spread = x1[0] - b*x2
            else:
                x1 = sm.add_constant(x1)
                results = sm.OLS(np.array(x2),np.array(x1)).fit()
                b = results.params[0]
                x2 = pd.DataFrame(x2)
                x1 = x1['const'] + x1[0]
                spread = x2[0] - b*x1
        except ValueError:
            b = 0
            spread = 0

    mu = spread.mean()
    return np.cumsum(spread), mu, b # the spread is a series (don't index it )

# this function will retruns a list with tuples of the (high_pair, low_pair) and another list of tuples containing (spread, mu)
def find_cointegrated_pairs(data): 
    print(data)
    data = data.sample(n=30, axis='columns')
    data0 = data
    n = data.shape[1]
    keys = data.keys()
    pairs = []
    pvalue_matrix = np.ones((n,n))
    for i in range(n):
        for j in range(i+1,n):
            s1 = data[keys[i]]
            s2 = data[keys[j]]
            result = coint(s1, s2)
            pvalue = result[1]
            pvalue_matrix[i, j] = pvalue
            if pvalue < 0.05:
                pairs.append((keys[i],keys[j]))
        print(pairs)
    df = pd.DataFrame(pairs)
    df.to_csv(r'data for trading\cointegrated_pairs.csv')
    organised_pairs = []
    synthetic_asset = []
    for pair in pairs:
        x = data0[pair[0]].mean() - data0[pair[1]].mean()
        if x < 0:
            y = pair[1]
            x = pair[0]
        else:
            y = pair[0]
            x = pair[1]
        organised_pairs.append((y, x))  
        spread, mu, b = construct_synthetic_price(x, y)
        print(spread)
        synthetic_asset.append((spread, [mu, b]))
    return organised_pairs, synthetic_asset

#combine all the universe and send that to the code
@_data.timer_decorator
def routine1(collection_present, collection_of_tickers):
    HIGH_LIQUIDITY_STOCKS = pd.read_csv(ps.join(ROOT_DIR,'trading bot','data for trading', 'HIGH_LIQUIDITY_prices.csv'))
    HIGH_LIQUIDITY_STOCKS = HIGH_LIQUIDITY_STOCKS.drop(['date'], axis=1)
    if collection_present:
        HIGH_LIQUIDITY_STOCKS = collection_of_tickers
    else:
        pass
    print(HIGH_LIQUIDITY_STOCKS)
    stationarity = check_for_stationarity(HIGH_LIQUIDITY_STOCKS)
    print(stationarity)
    stationary_stocks = Hurst_exponent_comparison_test(stationarity)
    print(stationary_stocks)
    data = []
    [data.append(i) for i in range(5000)]
    data = pd.DataFrame(data)
    for stock in stationary_stocks:
        try:
            data[stock[0]] = stock[1][0]
            print(stock)
        except ValueError:
            pass
        print(data)
    data.fillna(0, inplace=True)
    data.drop([0], axis=1, inplace=True)
    print('final data', data)
    data.to_csv(r'data for trading\stationary stocks returns.csv')

# make Ornstein–Uhlenbeck 
# test strategy on fake rolling data using a nomral dristribution 
# np.random.normal(mu_stock, volatility_stock)
# debug constructor not called properly!!
# that is 200 stocks to trade not 200 datapoints !!
filename = r'data for trading\streaming live prices.csv'
def plot_live_strategies(filename, strategy):
    if strategy == 1:
        data = pd.read_csv(filename)
        tickers = data.columns
        for i in range(len(tickers)):
            ticker = tickers[i]
            try:
                data['sma15'+ str(ticker)] = data[ticker].rolling(window=15).mean()
                data['sma50'+ str(ticker)] = data[ticker].rolling(window=50).mean()
                data[[ticker,'sma15'+ str(ticker),'sma50'+ str(ticker)]].plot()
                plt.show()
            except pd.core.base.DataError:
                pass
    elif strategy == 2:
        data = pd.read_csv(r'data for trading\cointegrated_pairs.csv')
        for i in range(len(data)):
            try:
                ticker1 = data['1'][i]
                ticker2 = data['0'][i]
                print(ticker1,ticker2)
                print(b)
                spread, mu ,b = construct_synthetic_price(ticker1, ticker2)
                plt.plot(spread)
                plt.axhline(mu, color='black')
                plt.show()
            except TypeError:
                pass

#plot_live_strategies(filename, 2)