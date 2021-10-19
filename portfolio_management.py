from orders import OrderEngine
import threading 
from time import sleep
import pandas as pd 
import datetime

oe = OrderEngine(0,'','')
conn = oe.conn
api = oe.api

@conn.on(r'^account_updates$')
async def on_account_updates(conn, channel, account):
    print('account', account)

@conn.on(r'^trade_updates$')
async def on_trade_updates(conn, channel, trade):
    print('trade', trade)

@conn.on(r'^AM.AAPL$')
async def on_minute_bars(conn, channel, bar):
    print('bars', bar)

def ws_start():
	conn.run(['account_updates', 'trade_updates','AM.AAPL'])

#start WebSocket in a thread
'''
ws_thread = threading.Thread(target=ws_start, daemon=True)
ws_thread.start()

epochtimes = [time for time in oe.portfolio_history.timestamp]
datetimes = []
for epochtime in epochtimes:
    datetimes.append(datetime.datetime.fromtimestamp(epochtime))

df = pd.DataFrame([i for i in range(len(oe.portfolio_history.profit_loss))])
df['Profit and Loss'] = pd.DataFrame(oe.portfolio_history.profit_loss)
df['datetime'] = pd.DataFrame(datetimes)
df['equity'] = pd.DataFrame(oe.portfolio_history.equity)
df.set_index('datetime',inplace=True)
df.drop([0],axis=1,inplace=True)
print(df)
#-------------------------------------------------------------------------------------------------------

#print(api.get_last_trade(symbol='TSLA'))

# Get the last 100 of our closed orders
closed_orders = api.list_orders(
    status='closed',
    limit=oe.account.daytrade_count,
    nested=True  # show nested multi-leg orders
)

print(closed_orders)
'''
def wait_for_market_open():
    clock = api.get_clock()
    if not clock.is_open:
        time_to_open = clock.next_open - clock.timestamp
        sleep(time_to_open.total_seconds())
    return clock

#-------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    while True: 
        clock = wait_for_market_open()
        #print(df)
        sleep(5)
 
