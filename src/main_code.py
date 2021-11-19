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
qf = cf.QuantFig(df, 
                #  title='GPRO', 
                #  legend='top'
                )
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
    df.figure(columns=['VWAP', 'Volume'],kind='bar')])
                )


# cf.iplot(fig)
fig.show()

# %%

df1 = cf.datagen.lines(4, mode='abc')
# %%
df1[['c', 'd']] = df1[['c', 'd']] * 100

fig = go.Figure(**tools.merge_figures([
    df1.figure(columns=['a', 'b']),
    df1.figure(columns=['c', 'd'], kind='bar')
])).set_axis(['c','d'], side='right')

cf.iplot(fig)
# %%
fig3 = go.Figure(data=go.Scatter(x=df.index, y=df.VWAP, mode='lines', name='VWAP'))
fig4 =go.Figure(data=[go.Candlestick(x=df.index, open=df.Open, high=df.High, low=df.Low, close=df.Close)])

# %%
fig4.update_layout(xaxis_rangeslider_visible=False, template='plotly_dark')
fig4.update_yaxes(side='right')
fig4.show()
# %%
fig3.show()
# %%
fig7 = go.Figure(**tools.merge_figures([
    fig3,
    fig4
]))
# %%
fig7.update_layout(template='plotly_dark')
fig7.show()
# %%
fig10 = df.figure(columns=['VWAP'],kind='line')
fig10.update_yaxes(side='right')
fig10.show()
# %%
fig = go.Figure(**tools.merge_figures([
    qf.figure(),
    df.figure(columns=['VWAP'],kind='line').update_yaxes(side='right')
    
    ]))
    
# %%
fig.show()
# %%
