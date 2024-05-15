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

mgr = dm.BbgDataManager()

start_date = (datetime.today() - relativedelta(years=5)).strftime('%Y-%m-%d')
end_date = datetime.today().strftime('%Y-%m-%d')

sids = ["USDSEK Curncy","USDNOK Curncy",]

# pdf = PdfPages('my_plots.pdf')
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

    results[sid] = df


# print(usdsek_df)

# for sid in sids:
#     print(results[sid]['PX_LAST'])

# Create a list of the 'PX_LAST' columns
px_last_columns = [results[sid]['PX_LAST'] for sid in sids]

# Concatenate the 'PX_LAST' columns
df_main = pd.concat(px_last_columns, axis=1, keys=sids) 

print(df_main.tail())
# df.to_csv('my_data.csv', sheet_name=f'dataframe_{i}')





