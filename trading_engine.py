from sys import flags
from data_processing import DataProcessing
dp = DataProcessing([])
import numpy as np
import pandas as pd
import statistical_arbitrage as sttarb
from matplotlib import pyplot as plt
from orders import OrderEngine 
oe = OrderEngine(0,'','')
api = oe.api
from deep_learning_trading import DeepLearningStrategy, NeuralNetwork
from yahoo_fin.stock_info import get_live_price
import alpaca_trade_api


def observe_trading_activities(S,mu):
    plt.plot(S)
    plt.axhline(mu,color='black')
    plt.show()

def train_model():
    data = pd.read_csv(r'data for trading\stationary stocks returns.csv')
    data = data.sample(n=5,axis='columns')
    tickers = dp.clean_columns_and_dataframe(data)
    trade = DeepLearningStrategy(data)
    _ = trade.construct_dictionary_of_classes(tickers)
    training_data = trade.init_training_data()

    labels = 'classes'
    nnets = NeuralNetwork(2, labels, training_data, False)
    X, Y = nnets.clean_data()
    _ , acc = nnets.save_best_model(X,Y)
    print(acc)
    #nnets.iterate_predictions(X,Y)
    return tickers, data, trade

def init_flags_and_order_ids(filename):
    data = pd.read_csv(filename)
    tickers = dp.clean_columns_and_dataframe(data)
    for i in range(len(tickers)):
        ticker = tickers[i]
        flags = 0
        order_id = 0
        df = dp.dataframe_generator(i=[ticker,flags, order_id])
        df.to_csv(r'data for trading\dictionary flags and orders.csv')
    
def inusfficient_funds_exception(func, *a, **kw):
    def wrapper(*a, **kw):
        try:
            container = func(*a,*kw)
        except alpaca_trade_api.rest.APIError as err:
            container = None
            print(err)
        return container
    return wrapper

@inusfficient_funds_exception
def pairs_trading(S,mu,b,ticker2,ticker1):
    '''
    pairs = pd.read_csv(r'data for trading\cointegrated_pairs.csv')
    pairs = pairs.sample(n=200, axis='rows')
    print(pairs)
    x2 = []
    x1 = []
    for pair in pairs['0']:
        for p in pairs['1']:
            x2.append(pair)
            x1.append(p)
    for i in range(len(x2)):
        ticker2 = x2[i]
        ticker1 = x1[i]
        S, mu, b = sttarb.construct_synthetic_price(ticker1,ticker2)
        S = pd.DataFrame(S)
    '''
    for price in S.tail(1):
        if price > mu:

            try:
                price2 = get_live_price(ticker2)
            except AssertionError:
                price2 = 0
            oe = OrderEngine(price2,ticker2,'sell')
            oe.create_order()

            try:
                price1 = get_live_price(ticker1)
            except AssertionError:
                price1 = 0
            oe = OrderEngine(price1,ticker1,'buy')
            oe.create_order(qty=b)

        elif price < mu:

            try:
                price2 = get_live_price(ticker2)
            except AssertionError:
                price2 = 0
            oe = OrderEngine(price2,ticker2,'buy')
            oe.create_order()

            try:
                price1 = get_live_price(ticker1)
            except AssertionError:
                price1 = 0
            oe = OrderEngine(price1,ticker1,'sell')
            oe.create_order(qty=b)
        else:
            pass

@inusfficient_funds_exception      
def machine_learning_strategy(tickers, data, trade):
    for stock in tickers:
        X = data[stock]
        signal = trade.market_prediction(X)
        price = get_live_price(stock)
        oe = OrderEngine(price,stock,signal)
        oe.create_trailing_sl_order()

def crossover_strategy(filename):
    global dp

    data = pd.read_csv(filename)
    tickers = dp.clean_columns_and_dataframe(data)
    tickers.remove('datetime')
    for i in range(len(tickers)):
        ticker = tickers[i]
        print(ticker)
        dictionary_ticker = pd.read_csv(r'data for trading\dictionary flags and orders.csv')
        try:
            flag = dictionary_ticker[i][1]
            order_id = dictionary_ticker[i][2]
        except KeyError:
            flag = 0
            order_id = 0
        data['sma15'+ str(ticker)] = data[ticker].rolling(window=15).mean()
        data['sma50'+ str(ticker)] = data[ticker].rolling(window=50).mean()
        for price in data[ticker].tail(1):
            dp = DataProcessing(data[ticker])
            x = dp.find_location(price) - 1
            print(price)
            print('sma15:', data['sma15'+ str(ticker)][x])
            print('sma50:', data['sma50'+ str(ticker)][x])
            try:
                if data['sma50'+ str(ticker)][x] > data['sma15'+ str(ticker)][x]:
                    if flag != 1:
                        if flag == -1:
                            oe = OrderEngine(price,ticker,'buy')
                            oe.close_orders(order_id)
                            oe.create_trailing_sl_order()
                            dictionary_ticker[i][1] = 1
                        else:
                            dictionary_ticker[i][1] = 1
                            oe = OrderEngine(price,ticker,'buy')
                            order = oe.create_trailing_sl_order(get_order=True)
                            dictionary_ticker[i][2] = order.id
                    else:
                        pass

                elif data['sma50'+ str(ticker)][x] < data['sma15'+ str(ticker)][x]:
                    if flag != -1:
                        if flag == 1:
                            oe = OrderEngine(price,ticker,'sell')
                            oe.close_orders(order_id)
                            oe.create_trailing_sl_order()
                            dictionary_ticker[i][1] = -1 
                        else:
                            oe = OrderEngine(price,ticker,'sell')
                            order = oe.create_trailing_sl_order(get_order=True)
                            dictionary_ticker[i][2] = order.id
                            dictionary_ticker[i][1] = -1
                    else:
                        pass

                else:
                    pass
            except alpaca_trade_api.rest.APIError as err:
                print(err)
            except KeyError as err:
                print(err)
        
    dp.count_down(60)

