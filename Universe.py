import pandas as pd
from yahoo_fin.stock_info import get_day_gainers, get_day_losers, get_day_most_active, get_day_most_active, get_live_price
import twelve_data
import json
import schedule
import json
from data_processing import DataProcessing
dp = DataProcessing([])
from check_for_returns import get_daily_prices
import threading 
import portfolio_management as pm
import requests

api_key = '0Y7L7U4SDA8BGGLT'
api_key2 = 'RV2HIM59SOF7QQRR'
api_key3 = 'KOHCIVFRQUJ7MDV1'
api_key4 = ' H0C28Q4EK4T6VRI8'
stocks_price_data = r'data for trading\price data.csv'
fx_currency_pairs = r'data for trading\currency_pairs.csv'
routine_1_finished = True
class DataUniverse(DataProcessing):
    def __init__(self, time_period):  
        self.api_key = 'KOHCIVFRQUJ7MDV1'
        self.init_streaming = True
        self.time_period = time_period

    def context(self):
        clock = pm.wait_for_market_open()
        return clock

    def high_activity_initialization(self, u=True):
        h = get_day_gainers()
        b = get_day_losers()
        c = get_day_most_active()
        d = get_day_most_active()
        h = pd.DataFrame(h['Symbol'])
        h = self.series_to_list(h)

        b = b['Symbol']
        b = self.series_to_list(b)

        c = c['Symbol']
        c = self.series_to_list(c)

        d = d['Symbol']
        d = self.series_to_list(d)

        HIGH_ACTIVITY_STOCK = h + b + c
        HIGH_ACTIVITY_STOCKS = HIGH_ACTIVITY_STOCK + d
        HIGH_ACTIVITY_STOCKS = self.remove_repeats(HIGH_ACTIVITY_STOCKS)
        HIGH_ACTIVITY_STOCKS = pd.DataFrame(HIGH_ACTIVITY_STOCKS)
        filename = r'HIGH_ACTIVITY_STOCKS.csv'
        if u:
            HIGH_ACTIVITY_STOCKS.to_csv(filename)
        else:
            pass
        return HIGH_ACTIVITY_STOCKS

    def get_live_streaming_data(self, ticker,fx=False):
        try:
            price = get_live_price(ticker)
            if fx:
                price = twelve_data.get_real_time_data(ticker)
            else:
                pass
            
        except json.decoder.JSONDecodeError as jsencd:
            print(jsencd)
            try:
                price = twelve_data.get_real_time_data(ticker)
            except KeyError as kyerr:
                print(kyerr)
                price = 0
        
        except AssertionError:
            price = 0
        
        except requests.exceptions.ConnectionError:
            price = 0

        print(f' from get live streaming data : {ticker} {price}')

        return price 

    def _from_forex_tickers_to_price(self, ticker_filename,number_of_tickers, save=True):
        data = pd.read_csv(ticker_filename)
        data = data.drop(['Unnamed: 0'], axis=1)
        data = data.sample(frac=1)   
        time = self.get_datetime_from_twelve()
        time = self.series_to_list(time)
        data2 = pd.DataFrame(time)
        data2['datetime'] = data2[0]
        data2 = data2.drop([0], axis=1)
        for ticker in data['0'][0:number_of_tickers]:
            print(len(data['0']))
            print(ticker)
            ticker = ticker.replace('_','/') 
            data2[ticker] = get_daily_prices(ticker)
            print(data2)        
        if save == True:
            a = ticker_filename.replace('.csv', '_prices.csv')
            data2.to_csv(a)
            print(data2)
        else:
            return data2
        
    def from_stocks_tickers_to_price(self,tickers_filename):
        # refactor this code make sure there is no close
        df = pd.read_csv(tickers_filename)
        df.drop(['0','Unnamed: 0'],axis=1,inplace=True)
        ticks = df.columns
        data = get_daily_prices(ticks[len(ticks)-1])
        for tick in ticks:
            data[tick] = get_daily_prices(tick) 
        df.drop([ticks[len(ticks)-1]],axis=1,inplace=True)
        print(data)
        data.to_csv(stocks_price_data)
    
    def streaming_live_data(self):
        global routine_1_finished

        if routine_1_finished:
            if self.init_streaming:
                df = pd.read_csv(stocks_price_data)
                stock_dates = self.series_to_list(df['datetime'])
                stock_dates.reverse()

                df.set_index('datetime', inplace=True)

                print('''

                ----------------- START --------------------------------

                {}'''.format(df))

                tickers = self.series_to_list(df.columns)
                
                # conver into a dictionary that will map each ticker as key and the value 
                # is a list of prices so that you can easily append streaming data
                ticker_prices_dictionary = {}
                stock_dates.append('20{}'.format(self.get_rounded_date()))
                for ticker in tickers:
                    list__stock_prices = self.series_to_list(df[ticker])
                    price = self.get_live_streaming_data(ticker)
                    list__stock_prices.append(price)
                    ticker_prices_dictionary[ticker] = list__stock_prices

                final_data = pd.DataFrame(ticker_prices_dictionary)
                final_data['datetime'] = pd.DataFrame(stock_dates)
                final_data.set_index('datetime',inplace=True)
                print(final_data)
                final_data.to_csv(r'data for trading\streaming live prices.csv')
                self.init_streaming = False
            else:
                df = pd.read_csv(r'data for trading\streaming live prices.csv')
                stock_dates = self.series_to_list(df['datetime'])
                    
                print('''
                
                -------------------------------- NEW ITERATION ------------------------------
                
                '''.format(df))
                tickers = self.series_to_list(df.columns)
                        
                # conver into a dictionary that will map each ticker as key and the value 
                # is a list of prices so that you can easily append streaming data
                ticker_prices_dictionary = {}
                stock_dates.append('20{}'.format(self.get_rounded_date()))

                for ticker in tickers:
                    list__stock_prices = self.series_to_list(df[ticker])
                    price = self.get_live_streaming_data(ticker)
                    list__stock_prices.append(price)
                    ticker_prices_dictionary[ticker] = list__stock_prices

                final_data = pd.DataFrame(ticker_prices_dictionary)
                final_data['datetime'] = pd.DataFrame(stock_dates)
                
                final_data.set_index('datetime',inplace=True)
                print(final_data)
                final_data.to_csv(r'data for trading\streaming live prices.csv')
                self.count_down(60*self.time_period)
        else:
            pass

def routine2():
    
    uni = DataUniverse(1)
    
    if routine_1_finished:
        data = pd.read_csv(r'data for trading\stationary stocks returns.csv')
        tickers = dp.clean_columns_and_dataframe(data)
        price_data = get_daily_prices('TSLA')
        for ticker in tickers:
            prices = dp.series_to_list(get_daily_prices(ticker))
            prices.reverse()
            price_data[ticker] = pd.DataFrame(prices)
            print(price_data)
        price_data.to_csv(r'data for trading\price data.csv')
    else:
        pass

    t0 = threading.Thread(target=uni.streaming_live_data(), daemon=True)
    t0.start()
        
