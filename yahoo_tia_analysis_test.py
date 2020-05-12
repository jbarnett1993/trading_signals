import tia.analysis.ta as ta
import tia.analysis.talib_wrapper as talib
import pandas as pd
from pandas.io.data import get_data_yahoo
from tia.analysis.model import SingleAssetPortfolio, PortfolioPricer, load_yahoo_stock, PortfolioSummary
from tia.analysis.model.ret import RoiiRetCalculator
from tia.util.fmt import DynamicColumnFormatter, DynamicRowFormatter, new_dynamic_formatter
import matplotlib.pyplot as plt

# drop adj close & volume for example sake
msft = load_yahoo_stock('MSFT', start='1/1/2010')

