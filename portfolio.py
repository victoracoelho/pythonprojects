import numpy as np
import pandas as pd
from pandas_datareader import data as wb
import matplotlib.pyplot as plt

t1 = input('Digite o código da primeira ação: ')
t2 = input('Digite o código da segunda ação: ')
t3 = input('Digite o código da terceira ação: ')
t4 = input('Digite o código da quarta ação: ')
p1 = float(input('Digite o peso da primeira ação: '))
p2 = float(input('Digite o peso da segunda ação: '))
p3 = float(input('Digite o peso da terceira ação: '))
p4 = float(input('Digite o peso da quarta ação: '))

tickers = [t1, t2, t3, t4]
mydata = pd.DataFrame()
for t in tickers:
    mydata[t] = wb.DataReader(t, data_source='yahoo', start = '2000-1-1')['Adj Close']

(mydata / mydata.iloc[0] * 100).plot(figsize = (15, 6));
plt.show()

returns = (mydata / mydata.shift(1)) - 1
weights = np.array([p1, p2, p3, p4])

annual_returns = returns.mean() * 250
portfolio = str(round(np.dot(annual_returns, weights), 5) * 100) + ' %'
print(portfolio)
