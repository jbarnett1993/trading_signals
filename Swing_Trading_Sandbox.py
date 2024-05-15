import pandas as pd
import numpy as np
import tia.bbg.datamgr as dm
import tia.analysis.ta as ta
import tia.analysis.model as model
from matplotlib import gridspec
from datetime import datetime
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt

mgr = dm.BbgDataManager()

start_date = (datetime.today() - relativedelta(years=5)).strftime('%Y-%m-%d')
end_date = datetime.today().strftime('%Y-%m-%d')

sids = mgr["SPX Index"]


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


# Create a figure with two subplots, one for the price chart and another for the RSI chart
fig = plt.figure(figsize=(20, 10))
gs = gridspec.GridSpec(2, 1, height_ratios=[1, 0.25])
ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1], sharex=ax1)

fig.subplots_adjust(wspace=0, hspace=0)

# Plot the price chart
ax1.plot(df['PX_LAST'], label='PRICE', color='red')
ax1.plot(df['20dma'], label='20 Day Moving Average', color='orange')
ax1.plot(df['50dma'], label='50 Day Moving Average', color='blue')
ax1.plot(df['200dma'], label='200 Day Moving Average', color='pink')
ax1.grid(True, linestyle='--', alpha=0.5)

# Add markers for buy and sell signals
ax1.scatter(df.index[df['Signal'] == 'BUY'], df['PX_LAST'][df['Signal'] == 'BUY'], label='BUY', marker='^', color='green', s=200)
ax1.scatter(df.index[df['Signal'] == 'SELL'], df['PX_LAST'][df['Signal'] == 'SELL'], label='SELL', marker='v', color='red', s=200)

ax1.set_title('Swing Trading Chart')
ax1.set_ylabel('Price')
ax1.legend(loc='upper left')

# Plot the RSI chart
ax2.plot(df['RSI'], label='RSI', color='black')
ax2.legend(loc='upper left')
ax2.set_ylabel('RSI')
ax2.axhline(30,color = 'red', linewidth = 2)
ax2.axhline(50,color = 'red', linewidth = 2)
ax2.axhline(70,color = 'red', linewidth = 2)

#add markers on the RSI

ax2.scatter(df.index[df['Signal'] == 'BUY'], df['RSI'][df['Signal'] == 'BUY'], label='BUY', marker='^', color='green', s=200)
ax2.scatter(df.index[df['Signal'] == 'SELL'], df['RSI'][df['Signal'] == 'SELL'], label='SELL', marker='v', color='red', s=200)

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

#add percentage change of underlying for comparison
df['underlying % returns']= df['PX_LAST'].pct_change()*100

#print(df.tail())

#plot a chart of the cumulative returns

#plot chart
plt.figure(figsize=(20, 10))

plt.plot(df['Percent Returns'].cumsum())
plt.plot(df['underlying % returns'].cumsum())
plt.title('Swing Trading Strategy')
plt.xlabel('Date')
plt.ylabel('Cumulative Returns (%)')
# plt.show()



