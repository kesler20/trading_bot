from statistical_arbitrage import *
from check_for_returns import *
from trading_engine import *
import numpy as np
import pandas as pd
from data_processing import DataProcessing
dp = DataProcessing([])
from Universe import DataUniverse, routine2, routine_1_finished
ui = DataUniverse(1)

@dp.timer_decorator
def routine3():
    #get organised returns data for machine learning
    return_data = pd.read_csv(r'data for trading\stationary stocks returns.csv')
    tickers = dp.clean_columns_and_dataframe(return_data)
    
    organised_pairs, synthetic_asset = find_cointegrated_pairs(return_data)
    
    #get prices of stationary stock returns
    price_data = pd.read_csv(r'data for trading\streaming live prices.csv')

    tickers, data , trade = train_model()

    return tickers, trade, price_data, organised_pairs, synthetic_asset, data, return_data#(returns)

if __name__ == '__main__':
    collection_of_tickers = get_random_tickers(r'data for trading\Alpace tradable assets.csv',200)
    routine1(True,collection_of_tickers)
    routine2()
    tickers, trade, price_data, organised_pairs, synthetic_asset, data, return_data = routine3()
    filename = r'data for trading\streaming live prices.csv'
    init_flags_and_order_ids(filename)

    machine_learning_strategy(tickers, data, trade)

    while True:
        for i in range(len(organised_pairs)):
            x2 = organised_pairs[i][0]
            x1 = organised_pairs[i][1]
            S = synthetic_asset[i][0]
            mu = synthetic_asset[i][1][0]
            b = synthetic_asset[i][1][1]
            pairs_trading(S,mu,b,x2,x1)
        clock = ui.context()
        crossover_strategy(filename)