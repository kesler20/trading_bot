url_documents = 'https://pypi.org/project/oandapyV20/'
documentation = 'https://oanda-api-v20.readthedocs.io/en/latest/endpoints/orders/ordercreate.html'
trailing_stop_loss_documentation = 'https://developer.oanda.com/rest-live-v20/order-df/'

from oandapyV20.contrib.requests import MarketOrderRequest, marketorder
from oandapyV20.contrib.requests import TakeProfitDetails, StopLossDetails
import oandapyV20.endpoints.accounts as accounts
import oandapyV20.endpoints.orders as orders
import oandapyV20
import json
import saxo_openapi.endpoints.accounthistory as ah
from oandapyV20 import API    # the client
import oandapyV20.endpoints.trades as trades
import oandapyV20.endpoints.positions as positions
import oandapyV20.endpoints.pricing as pricing
import oandapyV20.endpoints.trades as trades
import oandapyV20.endpoints.orders as orders
import orders as od
accountID = '101-004-18284583-001'
token = '6d6c64b52aca41a871cec86322f34ea2-3382c3ea4fe182b8e9a8ffc4ce922f9d'

client = API(access_token=token)
api = oandapyV20.API(access_token=token)

def trade_list():
  r = trades.TradesList(accountID)
  rv = client.request(r)
  print("RESPONSE:\n{}".format(json.dumps(rv, indent=2)))
 
def create_fx_order(instrument, price, trade_won,side):
    TAKE_PROFIT, STOP_LOSS = od.generate_bracket_prices(price,side)
    units = od.KELLY_CRITERION(price, trade_won)
    mktOrder = MarketOrderRequest(
        instrument=instrument,
        units=units,
        takeProfitOnFill=TakeProfitDetails(price=TAKE_PROFIT).data,
        stopLossOnFill=StopLossDetails(price=STOP_LOSS).data
      )
    r = orders.OrderCreate(accountID, data=mktOrder.data)
    try:
        # create the OrderCreate request
        rv = api.request(r)
    except oandapyV20.exceptions.V20Error as err:
        print(r.status_code, err)
    else:
        print(json.dumps(rv, indent=2))

def Account_Change(transactionID):
  client = oandapyV20.API(access_token=token)
  params = {
    "sinceTransactionID": transactionID
  }
  r = accounts.AccountChanges(accountID=accountID, params=params)
  client.request(r)
  print(r.response)
  r = accounts.AccountDetails(accountID)
  client.request(r)
  print(r.response)

def Account_instruments_list(instruments_list):
  params = {
    "instruments": instruments_list
  }
  r = accounts.AccountInstruments(accountID=accountID, params=params)
  client.request(r)
  print(r.response)

'''
def check_historical_positions(from_date,to_date):
  params ={
    "FromDate": from_date,
    "ToDate": to_date
  }
  r = ah.historicalpositions.HistoricalPositions(
    params=params)
  client.request(r)
  print(json.dumps(r.response, indent=2))
'''
def Account_summary():
  client = oandapyV20.API(access_token=token)
  r = accounts.AccountSummary(accountID)
  client.request(r)
  print(r.response)

def cancel_order(orderID):
  client = oandapyV20.API(access_token=token)
  r = orders.OrderCancel(accountID=accountID, orderID=orderID)
  client.request(r)
  print(r.response)

def chekc_open_positions():
  client = oandapyV20.API(access_token=token)
  r = positions.OpenPositions(accountID=accountID)
  client.request(r)
  print(r.response)

def close_position_close(instrument):
  client = oandapyV20.API(access_token=token)
  data ={
    "longUnits": "ALL"
  }

  r = positions.PositionClose(
    accountID=accountID,
    instrument=instrument,
    data=data
  )
  client.request(r)
  print(r.response) 

def chekc_position_detalis(instrument):
  client = oandapyV20.API(access_token=token)
  r = positions.PositionList(accountID=accountID)
  client.request(r)
  print(r.response)
  client = oandapyV20.API(access_token=token)
  r = positions.PositionDetails(accountID=accountID, instrument=instrument)
  client.request(r)
  print(r.response)

def order_details(orderID):
  client = oandapyV20.API(access_token=token)
  r = orders.OrderDetails(accountID=accountID, orderID=orderID)
  client.request(r)
  print(r.response)

def price_streaming_data_with_liquidity(instruments):
  params ={
    "instruments": instruments
  }
  r = pricing.PricingStream(accountID=accountID, params=params)
  rv = api.request(r)
  maxrecs = 100
  for ticks in r:
      print(json.dumps(ticks, indent=4),",")
      if maxrecs == 0:
          r.terminate("maxrecs records received")

def check_open_trades():
  client = oandapyV20.API(access_token=token)
  r = trades.OpenTrades(accountID=accountID)
  client.request(r)
  print(r.response)

def trade_extension_request_order(TAKE_PROFIT,STOP_LOSS,tradeID):
  client = oandapyV20.API(access_token=token)
  data ={
    "takeProfit": {
              "timeInForce": "GTC",
              "price": TAKE_PROFIT
            },
    "stopLoss": {
              "timeInForce": "GTC",
              "price": STOP_LOSS
            }
  }

  r = trades.TradeCRCDO(
    accountID=accountID,
    tradeID=tradeID,
    data=data
  )

  client.request(r)
  print(r.response)

def check_trade_details(tradeID):
  client = oandapyV20.API(access_token=token)
  r = accounts.TradeDetails(accountID=accountID, tradeID=tradeID)
  client.request(r)
  print(r.response)

def check_list_of_trades(instruments):
  client = oandapyV20.API(access_token=token)
  params ={
    "instrument": instruments
  }

  r = trades.TradesList(accountID=accountID, params=params)
  client.request(r)
  print(r.response)

def replace_order(orderID,units,instrument,price):
  client = oandapyV20.API(access_token=token)
  data ={
            "order": {
              "units": units,
              "instrument": instrument,
              "price": price,
              "type": "LIMIT"
            }
  }

  r = orders.OrderReplace(accountID=accountID, orderID=orderID, data=data)
  client.request(r)
  print(r.response)

from datetime import datetime, timedelta

# sample account_id
account_id = 1813880

# set the trade to expire after one day
trade_expire = datetime.utcnow() + timedelta(days=1)
trade_expire = trade_expire.isoformat("T") + "Z"

response = oanda.create_order(account_id,
    instrument="USD_CAD",
    units=1000,
    side='sell',
    type='limit',
    price=1.15,
    expiry=trade_expire
)
