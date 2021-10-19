from trading_engine import *
from data_processing import DataProcessing
dp = DataProcessing([])


filename = r'data for trading\streaming live prices.csv'
init_flags_and_order_ids(filename)

while True:
    crossover_strategy(filename)