import tia.analysis.ta as ta
import tia.analysis.talib_wrapper as talib
import pandas as pd
from pandas_datareader import get_data_yahoo
from tia.analysis.model import SingleAssetPortfolio, PortfolioPricer, load_yahoo_stock, PortfolioSummary
from tia.analysis.model.ret import RoiiRetCalculator
from tia.util.fmt import DynamicColumnFormatter, DynamicRowFormatter, new_dynamic_formatter
import matplotlib.pyplot as plt

# drop adj close & volume for example sake 
msft = load_yahoo_stock('MSFT', start='1/1/2010')

# build signal when 50d crosses 200d
moving_avgs = pd.DataFrame({'50': ta.sma(msft.pxs.close, 50), '200': ta.sma(msft.pxs.close, 200)})
signal = ta.cross_signal(moving_avgs['50'], moving_avgs['200']).dropna()
# keep only entry
entry_signal = signal.copy()
entry_signal[signal.shift(1) == signal]  = 0 
entry_signal = entry_signal[entry_signal != 0]
# show when the signal triggers
moving_avgs.plot(color=['b', 'k'], title='MSFT moving averages')
for i, v in entry_signal.iteritems():
    if v == -1:
        plt.plot(i, moving_avgs['50'][i], 'rv')
    else:
        plt.plot(i, moving_avgs['50'][i], 'k^')