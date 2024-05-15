import pandas as pd
import numpy as np
import tia.bbg.datamgr as dm
import tia.analysis.ta as ta
import tia.analysis.model as model
from datetime import datetime
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt

mgr = dm.BbgDataManager()

start_date = (datetime.today() - relativedelta(years=5)).strftime('%Y-%m-%d')
end_date = datetime.today().strftime('%Y-%m-%d')

sids = mgr["EURUSD Curncy"]


mgr.sid_result_mode = 'frame'

df = sids.get_historical(['PX_LAST'], start_date, end_date)

# calculate the moving averages
df['20dma'] = df['PX_LAST'].rolling(window=20).mean()
df['50dma'] = df['PX_LAST'].rolling(window=50).mean()
df['200dma'] = df['PX_LAST'].rolling(window=200).mean()
df['RSI']= ta.RSI(df['PX_LAST'],n=14)

#generate the buy and sell signals
signals = []
for i in range(0, len(df)):
    if (df['20dma'][i] > df['50dma'][i]) and (df['20dma'][i-1] < df['50dma'][i-1]) and df['RSI'][i] < 50:
        signals.append('BUY')
    elif (df['50dma'][i] > df['200dma'][i]) and (df['50dma'][i-1] < df['200dma'][i-1]) and df['RSI'][i] < 50:
        signals.append('BUY')
    elif (df['50dma'][i] < df['200dma'][i]) and (df['50dma'][i-1] > df['200dma'][i-1]) and df['RSI'][i] > 50:
        signals.append('SELL')
    else:
        signals.append('HOLD')
# add the signals to the dataframe
df['Signal'] = signals

#calculate the position we have
position = 0
positions = []
for i in range(0, len(df)):
    if df['Signal'][i] == 'BUY':
        position += 1
    elif df['Signal'][i] == 'SELL':
        position -= 1
    else:
        position = position
    positions.append(position)
df['Position'] = positions

print(df)


# plot a chart that shows the moving averages and also the points at which we would buy and sell
plt.figure(figsize=(20, 10))
# Plot the Price chart
plt.subplot(2, 1, 1)
plt.plot(df['PX_LAST'], label='PRICE', color='red')
plt.plot(df['20dma'], label='20 Day Moving Average', color='orange')
plt.plot(df['50dma'], label='50 Day Moving Average', color='blue')
plt.plot(df['200dma'], label='200 Day Moving Average', color='pink')
plt.grid(True, linestyle='--', alpha=0.5)

# add markers for buy and sell signals
plt.scatter(df.index[df['Signal'] == 'BUY'], df['PX_LAST'][df['Signal'] == 'BUY'], label='BUY', marker='^', color='green',s=100)
plt.scatter(df.index[df['Signal'] == 'SELL'], df['PX_LAST'][df['Signal'] == 'SELL'], label='SELL', marker='v', color='red',s=100)

plt.title('Swing Trading Chart')
# plt.xlabel('Date')
plt.ylabel('Price')
plt.legend(loc='upper left')

# Plot the RSI chart
ax2 = plt.subplot(2, 1, 2)
ax2.plot(df['RSI'], label='RSI', color='black')
# plt.title('RSI Chart')
plt.legend(loc='upper left')
plt.show()

#calculate the returns of the trading strategy

def calculate_returns(df):
    returns = []
    for i in range(0, len(df)):
        if df['Position'][i] == 0:
            returns.append(0.0)
        else:
            returns.append(df['Position'][i] * (df['PX_LAST'][i] - df['PX_LAST'][i-1]))
    return returns

df['Returns'] = calculate_returns(df)

#calcuate the percentage returns
def calculate_percent_returns(df):
    percent_returns = []
    for i in range(0, len(df)):
        if df['Position'][i] == 0:
            percent_returns.append(0.0)
        else:
            percent_returns.append(df['Position'][i] * 100 *((df['PX_LAST'][i] - df['PX_LAST'][i-1]) / df['PX_LAST'][i-1]))
    return percent_returns

df['Percent Returns'] = calculate_percent_returns(df)

#add percentage change of index for comparison
df['Index % returns']= df['PX_LAST'].pct_change()*100

#print(df.tail())

#plot a chart of the cumulative returns

#plot chart
plt.figure(figsize=(20, 10))

plt.plot(df['Percent Returns'].cumsum())
plt.plot(df['Index % returns'].cumsum())
plt.title('Swing Trading Strategy')
plt.xlabel('Date')
plt.ylabel('Cumulative Returns (%)')
plt.show()



