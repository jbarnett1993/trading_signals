import pandas as pd
import numpy as np
import tia.bbg.datamgr as dm
import tia.analysis.ta as ta
import tia.analysis.model as model
from matplotlib import gridspec
from datetime import datetime
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

#calcuate the percentage returns
def calculate_percent_returns(df):
    percent_returns = []
    for i in range(0, len(df)):
        if df['Position'][i] == 0:
            percent_returns.append(0.0)
        else:
            percent_returns.append(df['Position'][i] * 100 *((df['PX_LAST'][i] - df['PX_LAST'][i-1]) / df['PX_LAST'][i-1]))
    return percent_returns


mgr = dm.BbgDataManager()

start_date = (datetime.today() - relativedelta(years=5)).strftime('%Y-%m-%d')
end_date = datetime.today().strftime('%Y-%m-%d')

sids = ["USDSEK Curncy","USDNOK Curncy","USDDKK Curncy","USDCHF Curncy","USDCAD Curncy",
            "USDJPY Curncy","EURSEK Curncy"]

pdf = PdfPages('my_plots.pdf')
# create an empty dataframe to store the results
results = {}

# iterate over the list of securities
for sid in sids:
    # get the historical data for the current security
    df = mgr.get_historical(sid, ['PX_LAST'], start_date, end_date)
    # calculate the moving averages and RSI
    df['20dma'] = df['PX_LAST'].rolling(window=20).mean()
    df['50dma'] = df['PX_LAST'].rolling(window=50).mean()
    df['200dma'] = df['PX_LAST'].rolling(window=200).mean()
    df['RSI']= ta.RSI(df['PX_LAST'],n=14)
    # generate the buy and sell signals
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

    # calculate the positions
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

    df['Percent Returns'] = calculate_percent_returns(df)

    results[sid] = df


# Create a list of the 'PX_LAST' columns
pct_return_columns = [results[sid]['Percent Returns'] for sid in sids]

# Concatenate the 'PX_LAST' columns
df_main = pd.concat(pct_return_columns, axis=1, keys=sids) 


# Calculate the sum of all the columns
total_returns = df_main.sum(axis=1)

# Add the 'total_returns' column to the dataframe
df_main = df_main.assign(total_returns=total_returns)

df_main.to_csv('total_returns.csv')


# print(df_main.tail())

#add percentage change of underlying for comparison
df['underlying % returns']= df['PX_LAST'].pct_change()*100

#print(df.tail())

# #plot a chart of the cumulative returns

# #plot chart
# plt.figure(figsize=(20, 10))

# plt.plot(df_main['total_returns'].cumsum())
# # plt.plot(df['underlying % returns'].cumsum())
# plt.title('Swing Trading Strategy')
# plt.xlabel('Date')
# plt.ylabel('Cumulative Returns (%)')
# plt.show()






