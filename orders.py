import requests, json
from config import *
import alpaca_trade_api as tradeapi
import time
import pandas as pd
import datetime
# for more documentation you can check https://algotrading101.com/learn/alpaca-trading-api-guide/

class OrderEngine(object):

    def __init__(self, price, symbol, side):
        self.price = price
        self.symbol = symbol
        self.side = side
        BASE_URL = "https://paper-api.alpaca.markets"
        self.ACCOUNT_URL = "{}/v2/account".format(BASE_URL)
        self.ORDERS_URL = "{}/v2/orders".format(BASE_URL)
        self.HEADERS = {'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': SECRET_KEY}
        self.api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL, api_version='v2')
        self.account = self.api.get_account()
        self.balance = self.account.cash 
        self.conn = tradeapi.stream2.StreamConn(API_KEY, SECRET_KEY, BASE_URL)
        self.positions_list = self.api.list_positions()
        self.portfolio_history = self.initinalise_portfolio_history()
        self.qty = self.KELLY_CRITERION()
    

    def initinalise_portfolio_history(self):
        todays_date = datetime.date.today()
        
        day = int(todays_date.strftime('%d'))
        if day < 10:
            day = int(todays_date.strftime('%d')[1]) 
            day = '0' + str(day)

        month = int(todays_date.strftime('%m'))
        if month < 10:
            month = str(todays_date.strftime('%m'))

        try:
            portfolio_history = self.api.get_portfolio_history(
                date_end='2021-{}-{}'.format(month,day),
                period='1D',
                timeframe='5Min'
            )
            print('2021-{}-{}'.format(month,day))
        except requests.exceptions.ConnectionError as err: 
            print(err)
            portfolio_history = ''
        return portfolio_history

    def initialise_universe(self):
        #cancel all orders before end of the day
        self.api.close_all_positions()
        # a bunch of other api calls that can be useful
        self.api.cancel_all_orders()
        #create a random watchlist
        universe = self.api.create_watchlist()
        print(self.account)
        print(self.balance) 
        print(universe)
        return universe
        # if you want to know the leverage
        #print(api.get_account_configurations())

    def initialise_alpaca_universe(self):
        assets = self.api.list_assets()
        assets_list = []
        for asset in assets:
            assets_list.append(asset.symbol)
        df = pd.DataFrame(assets_list)
        df.to_csv('Alpace tradable assets.csv')

    def update_probability_w(self):
        trade_won = 0
        day_trade_count = self.account.daytrade_count
        # you can access portfolio history from the database

        for p_and_l in self.portfolio_history.profit_loss:
            try:
                if p_and_l > 0:
                    trade_won += 1
                else:
                    pass
            except TypeError:
                pass
        p_w = trade_won/day_trade_count
        return p_w

    # kelly criterion assumes that returns are stationary
    def KELLY_CRITERION(self):
        try:
            p_w = self.update_probability_w()
        except ZeroDivisionError:
            p_w = 0.5
        p_l = 1 - p_w
        lot_size = (2*p_w - p_l)/2
        try:
            qty = (lot_size*float(self.balance))/self.price
            qty = round(qty)
        except ZeroDivisionError:
            qty = 0
        except ValueError:
            qty = 1
        except OverflowError:
            qty = 1
        #UHEWRBVIUWBVQIUVBQPOIUVQOIUBVQIUBQIUBVOIUEQRBNQIUBVNOIUQBVLQI
        qty = 1
        return qty

    def get_account(self):
        r = requests.get(self.ACCOUNT_URL, headers=self.HEADERS)

        return json.loads(r.content)

    def create_order(self,qty=0, time_in_force='gtc'):
        if qty == 0:
            pass
        else:
            self.qty = qty
        types = 'market'
        if self.side == 'buy':
            order = self.api.submit_order(
                self.symbol,
                self.qty,
                self.side, 
                types,
                time_in_force, 
                order_class='bracket',
                stop_loss={'stop_price': 0.995*self.price}, 
                take_profit={'limit_price': 1.01*self.price}
            )
        elif self.side == 'sell':
            order = self.api.submit_order(
                self.symbol,
                self.qty,
                self.side, 
                types,
                time_in_force, 
                order_class='bracket',
                stop_loss={'stop_price': 1.005*self.price}, 
                take_profit={'limit_price': 0.99*self.price}
            )
        else:
            print('what is the side')
        print(order)
        time.sleep(1)

    def get_orders(self):
        r = requests.get(self.ORDERS_URL, headers=self.HEADERS)

        return json.loads(r.content)

    # Submit a trailing stop order to sell 1 share of Apple at a
    # trailing stop of
    def create_trailing_sl_order(self, get_order=False):
        order = self.api.submit_order(
            symbol=self.symbol,
            qty=self.qty,
            side=self.side,
            type='trailing_stop',
            trail_percent=0.4,  # stop price will be hwm*0.996
            time_in_force='gtc',
        )
        if get_order:
            return order
        else:
            pass

    def get_order_by_id(self):
        # Submit a market order and assign it a Client Order ID.
        self.api.submit_order(
            symbol='AAPL',
            qty=1,
            side='buy',
            type='market',
            time_in_force='gtc',
            client_order_id='my_first_order'
        )

        # Get our order using its Client Order ID.
        my_order = self.api.get_order_by_client_order_id('my_first_order')
        print('Got order #{}'.format(my_order.id))
    
    def portfolio_history_error(self, func):
        def wrapper(*a,**kw):
            try:
                container = func(*a,**kw)
            except tradeapi.rest.APIError as err:
                print(err)
                container = None
            return container
        return wrapper

    def close_orders(self,order_id):
        self.api.cancel_order(order_id=order_id)