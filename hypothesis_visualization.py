import pandas as pd
from pandas.core import series
from data_processing import DataProcessing as dp
from matplotlib import pyplot as plt
import Universe as ui
import numpy as np
from numpy.core.function_base import linspace
from matplotlib import cm

def view_synthetic_price_and_mu(ticker1, ticker2, outputsize):
    synthetic_asset, mu, beta = ui.construct_synthetic_price(ticker1, ticker2, outputsize)
    synthetic_asset.plot()
    plt.axhline(mu, color='black')


def graphing_calculator(xlablel='X',ylablel='Y',zlablel='Z'):
    fxy = lambda x, y: x**2 - y**2
    X = linspace(0,10000)
    Y = linspace(0,10000)
    X1, Y1 = np.meshgrid(X,Y)
    F = fxy(X1,Y1)
    print(F)
    fig = plt.figure(figsize = [12,8])
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, F, cmap=cm.coolwarm)
    #plt.scatter(Z1,z3,z2,c='black', marker='o', alpha=0.9)
    ax.set_xlabel(xlablel)
    ax.set_ylabel(ylablel)
    ax.set_zlabel(zlablel)
    plt.show()

data = pd.read_csv(r'data for trading\data_with_sma_and_rsi.csv')

DIFF = []
for x in range(len(data)):
    difference = data['sma20 CWB'][x] - data['sma200 CWB'][x]
    DIFF.append(difference)

for diff in DIFF[0:255]:
    DIFF.remove(diff)

fx = pd.DataFrame(DIFF)
fx_mean = fx*fx

position_of_alpha1 = []
position_of_alpha2 = []
flag = -1
for x in range(len(data)):
    difference = data['sma20 CWB'][x] - data['sma200 CWB'][x]
    if difference > np.sqrt(fx_mean.mean()[0]) and flag != 1:
        position_of_alpha1.append(data['CWB'][x])
        flag = 1
    elif difference < -np.sqrt(fx_mean.mean()[0]) and flag != 0:
        position_of_alpha2.append(data['CWB'][x])
        flag = 0       
    else:
        position_of_alpha1.append(np.nan)
        position_of_alpha2.append(np.nan)

data['buy'] = pd.DataFrame(position_of_alpha1)
data['sell'] = pd.DataFrame(position_of_alpha2)
plt.plot(data['Unnamed: 0'], data[['CWB']], alpha=0.3)
plt.scatter(data['Unnamed: 0'], data['buy'],color='green', marker='^', alpha=1)
plt.scatter(data['Unnamed: 0'], data['sell'],color='red', marker='v', alpha=1)
plt.show()

plt.plot(DIFF)
plt.axhline(np.sqrt(fx_mean.mean()[0]), color='black')
plt.axhline(-np.sqrt(fx_mean.mean()[0]), color='black')
plt.show()

data = data[0:800]
plt.plot(data['0'], data[['CWB','sma20 CWB','sma200 CWB']])
plt.xticks(rotation=45)
plt.show()

data['difference'] = fx + (data['CWB'].mean())
data[['CWB','difference']].plot()
plt.show() 


