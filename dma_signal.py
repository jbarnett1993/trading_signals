from tia.bbg import LocalTerminal
import matplotlib
import matplotlib.pyplot as plt
import tia.analysis.ta as ta
import pandas as pd


# Single SID, Multiple Valid Fields
resp = LocalTerminal.get_historical(['EURUSD Curncy'], ['PX_LAST'], start='1/1/2019', end='05/11/2020')
df = resp.as_frame()

# Add the 30 and 50 day rolling averages

df['eurusd30dma'] = df['EURUSD Curncy']['PX_LAST'].rolling(window=30).mean()
df['eurusd50dma'] = df['EURUSD Curncy']['PX_LAST'].rolling(window=50).mean()

# Add the trading signals when the 30 day crosses the 50 day MA
signal = ta.cross_signal(df['eurusd30dma'], df['eurusd50dma']).dropna()

#only keep the entry/exit signals

entry_signal = signal.copy()
entry_signal[signal.shift(1) == signal]  = 0
entry_signal = entry_signal[entry_signal != 0]

#df['signal'] = entry_signal
matplotlib.style.use('ggplot')
df.plot(title='signals')
for i, v in entry_signal.iteritems():
    if v == -1:
        plt.plot(i, df['eurusd30dma'][i], 'rv')
    else:
        plt.plot(i, df['eurusd30dma'][i], 'k^')

#df.to_csv(r'C:\Users\barnjam\OneDrive - Manulife\trading_signals\CSV Outputs\signals.csv',index = False)
plt.show()

#df['usdjpy30dma'] = df['USDJPY Curncy']['PX_LAST'].rolling(window=30).mean()

#b = df['EURUSD Curncy']['PX_LAST'].plot()
matplotlib.style.use('ggplot')

#ax = df.plot(kind='line', title ="EURUSD Curncy PX", figsize=(15, 10), legend=True, fontsize=12)
#ax.set_xlabel("Date", fontsize=12)
#ax.set_ylabel("PX", fontsize=12)
#plt.show()
print(df.tail())



#TODO: Loop through the ccy's and return the dma for each one
#TODO: sepearate sheet for each ccy?
#TODO: most efficient way to have multiple ccy's in here and to generate a table output on when to trade
