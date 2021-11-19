# Finance playground
# %% 
%load_ext autotime
# %%
import pandas as pd
import numpy as np
from plotly.offline import init_notebook_mode
import yfinance as yf 

# %%
df = yf.download('GPRO', start='2000-01-01', end='2020-04-01', progress=False)

# %%
df.head(20)
# %%
# create a candlestick plot 
import cufflinks as cf 
import chart_studio.plotly as py
from plotly.offline import iplot
init_notebook_mode(connected=True)
cf.go_offline()
cf.set_config_file(theme='space', offline=False, world_readable=True)
# %%
print("List of Cufflinks Themes :",cf.getThemes())
# %%
qf = cf.QuantFig(df, title='GPRO', legend='top')
# qf.add_volume()
# qf.add_sma(periods=3, column='Close', color='red')
# qf.add_ema(periods=3, color='blue')
# qf.add_bollinger_bands()
qf.iplot()

# %%
# laziness involves install technical analysis library to add VWAP column to a data frame
from ta.volume import VolumeWeightedAveragePrice 

# %%    
def vwap (dataframe, window=3,fillna=True):
    vwap = VolumeWeightedAveragePrice(high=dataframe['High'],
                                      low=dataframe['Low'],
                                      close=dataframe['Close'],
                                      volume=dataframe['Volume'],window=window,fillna=fillna)
    dataframe['VWAP'] = vwap.volume_weighted_average_price()
    return dataframe

df = vwap(df)
# %%
df.head(20)
# %%
from cufflinks import tools 
import plotly.graph_objects as go
fig = go.Figure(**tools.merge_figures([
    qf.figure(),
    df.figure(columns=['VWAP'],kind='scatter')]))



fig.show()
# %%
test = df.iplot(kind='line', x=df.index,y=df.VWAP,title='VWAP')
# %%
