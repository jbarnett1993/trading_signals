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

sids = ["USDSEK Curncy","USDNOK Curncy","USDDKK Curncy","USDCHF Curncy","USDCAD Curncy",
            "USDJPY Curncy","EURSEK Curncy","EURNOK Curncy","EURDKK Curncy","EURCHF Curncy","EURNZD Curncy",
            "EURAUD Curncy","EURCAD Curncy","EURGBP Curncy","EURJPY Curncy","EURUSD Curncy","GBPSEK Curncy",
            "GBPNOK Curncy","GBPDKK Curncy","GBPCHF Curncy","GBPNZD Curncy","GBPAUD Curncy","GBPCAD Curncy",
            "GBPJPY Curncy","GBPUSD Curncy","CADSEK Curncy","CADNOK Curncy","CADDKK Curncy","CADCHF Curncy",
            "CADJPY Curncy","CADEUR Curncy","CADUSD Curncy","AUDSEK Curncy","AUDNOK Curncy","AUDDKK Curncy",
            "AUDCHF Curncy","AUDNZD Curncy","AUDCAD Curncy","AUDGBP Curncy","AUDJPY Curncy","AUDUSD Curncy",
            "NZDSEK Curncy","NZDNOK Curncy","NZDDKK Curncy","NZDCHF Curncy","NZDAUD Curncy","NZDCAD Curncy",
            "NZDGBP Curncy","NZDJPY Curncy","NZDUSD Curncy","CHFJPY Curncy","NOKSEK Curncy",]
            
            
            # "WN1 Comdty","US1 Comdty",
            # "UXY1 Comdty","TY1 Comdty","FV1 Comdty","TU1 Comdty","CA1 Comdty","UB1 Comdty","RX1 Comdty","OE1 Comdty",
            # "DU1 Comdty","G 1 Comdty","IK1 Comdty","OAT1 Comdty","BTS1 Comdty","BTO1 Comdty","JB1 Comdty","XM1 Comdty",
            # "YM1 Comdty","DM1 Index","ES1 Index","NQ1 Index","PT1 Index","IS1 Index","BZ1 Index","VG1 Index","Z 1 Index",
            # "CF1 Index","GX1 Index","IB1 Index","ST1 Index","EO1 Index","QC1 Index","SM1 Index","NK1 Index","HI1 Index","IFB1 Index",
            # "XP1 Index","CL1 Comdty"]

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

    ax1.set_title(sid)
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


    # save the chart to a PDF file
    pdf.savefig()

    # clear the current plot
    plt.clf()
    plt.close()

    # add the current dataframe to the dictionary using the security ID as the key
    results[sid] = df

pdf.close()



# get the dataframe for EURUSD Curncy
# eurusd_df = results['EURUSD Curncy']

# get the dataframe for SPX Index
# spx_df = results['SPX Index']

# print(eurusd_df.tail())

# print(spx_df.tail())


