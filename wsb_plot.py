import matplotlib.pyplot as plt
import plotly.graph_objects as go
from iexfinance.stocks import get_historical_data
import pandas as pd

def get_mean(df):
    mean_scores = df.groupby(['Date']).mean()
    mean_scores = mean_scores.xs('compound', axis="columns").transpose()
    return mean_scores

def plot_scores(df, title, symbol):
    mean_scores = get_mean(df)
    start = df['Date'].min()
    end = df['Date'].max()
    stock_output = get_historical_data(symbol, start, end, output_format='pandas',token = 'sk_fd1d80421fcf4ef0b1f040456646edd2')
    plt.rcParams['figure.figsize'] = [10, 6]
    ax = mean_scores.plot(kind='bar', color = 'r', label='score')
    ax2 = stock_output['close'].plot(secondary_y=True, use_index=False, label = 'price')
    fig = go.Figure(data=[go.Candlestick(x=stock_output['label'], open=stock_output['open'],low=stock_output['low'],high=stock_output['high'],close=stock_output['close'], yaxis='y1'),
                            go.Scatter(x= stock_output['label'], 
                                        y = mean_scores, yaxis='y2')
                        ])
    fig.update_layout(title='Sentiment level with stock price',
                       yaxis=dict(title='Price'),
                       yaxis2=dict(title='Sentiment compound',
                                   overlaying='y',
                                   side='right'))
    fig.show()
   

