from tia.bbg import LocalTerminal
import matplotlib
import matplotlib.pyplot as plt
import tia.analysis.ta as ta
import pandas as pd


# Single SID, Multiple Valid Fields
resp = LocalTerminal.get_historical(['EURUSD Curncy'], ['PX_LAST'], start='1/1/2020', end='10/28/2020')
df = resp.as_frame()

# Add the 30 and 50 day rolling averages

df['eurusd30dma'] = df['EURUSD Curncy']['PX_LAST'].rolling(window=30).mean()
df['eurusd50dma'] = df['EURUSD Curncy']['PX_LAST'].rolling(window=50).mean()

# Add the trading signals when the 30 day crosses the 50 day MAsasasas
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
        plt.plot(i, df['EURUSD Curncy']['PX_LAST'][i],'rv')
    else:
        plt.plot(i, df['EURUSD Curncy']['PX_LAST'][i],'k^')

#df.to_csv(r'C:\Users\barnjam\OneDrive - Manulife\trading_signals\CSV Outputs\signals.csv',index = False)
#plt.show()

# Can get the set of trades created by this signal
trades = ta.Signal(signal).close_to_close(df['EURUSD Curncy']['PX_LAST'])
trades

#TODO: most efficient way to have multiple ccy's in here and to generate a table output on when to trade