import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.ticker as mtick
import matplotlib.lines as mlines
import pandas as pd
import statsmodels.api as sm

plt.rcParams['figure.dpi'] = 227

gain = lambda x: x if x > 0 else 0
loss = lambda x: abs(x) if x < 0 else 0


def display_predictions():
    pass


def stock_charts(stock):

    plt.figure(figsize=(15, 10))
    # remove borders
    # plt.rcParams['axes.spines.left'] = False
    # plt.rcParams['axes.spines.right'] = False
    # plt.rcParams['axes.spines.top'] = False
    # plt.rcParams['axes.spines.bottom'] = False

    # create an empty grid
    gs = gridspec.GridSpec(5, 1, height_ratios=[3, 1, 1, 1, 1], hspace=0.1)

    # candlestick chart
    ax0 = plt.subplot(gs[0])
    ax0.yaxis.grid(False)
    ax0.xaxis.grid(True)
    # define width of candlestick elements
    width = .4
    width2 = .05
    # define up and down prices
    up = stock[stock.Close >= stock.Open]
    down = stock[stock.Close < stock.Open]
    # define colors to use
    up_color = 'green'
    down_color = 'red'
    # plot up prices
    plt.bar(up.index, up.Close - up.Open, width, bottom=up.Open, color=up_color)
    plt.bar(up.index, up.High - up.Close, width2, bottom=up.Close, color=up_color)
    plt.bar(up.index, up.Low - up.Open, width2, bottom=up.Open, color=up_color)
    # plot down prices
    plt.bar(down.index, down.Close - down.Open, width, bottom=down.Open, color=down_color)
    plt.bar(down.index, down.High - down.Open, width2, bottom=down.Open, color=down_color)
    plt.bar(down.index, down.Low - down.Close, width2, bottom=down.Close, color=down_color)
    # plt.xticks([])
    plt.tick_params('x', labelbottom=False)

    # Bollinger Band
    ax1 = plt.subplot(gs[1], sharex=ax0)
    ax1.grid(visible=True)
    ax1.yaxis.grid(False)
    ax1.xaxis.grid(True)
    ax1.set_facecolor('#e9ecef')
    plt.plot(stock.index, stock.Close, color='#3388cf', label='Price')
    ax1.legend(loc="upper right")
    plt.plot(stock.index, stock.MA21, color='#ad6eff', label='Moving Average (21 days)')
    ax1.legend(loc="upper right")
    plt.plot(stock.index, stock.Upper_band, color='#264653', alpha=0.3, label='Bollinger Band 2 STD')
    ax1.legend(loc="upper right", fontsize=8)
    plt.plot(stock.index, stock.Lower_band, color='#ffa33f', alpha=0.3)
    plt.fill_between(stock.index, stock.Upper_band, stock.Lower_band, color='#ffa00f', alpha=0.1,
                     label='Bollinger Band ({} STD)'.format(2))
    plt.tick_params('x', labelbottom=False)

    # MACD
    ax2 = plt.subplot(gs[2], sharex=ax1)
    ax2.set_facecolor('#caf0f8')
    plt.plot(stock.MACD, label='MACD', color='#b278ff')
    ax2.legend(loc="upper right")
    plt.plot(stock.Signal, label='Signal', color='#ffa74a')
    ax2.legend(loc="upper right")
    ax2.yaxis.grid(False)
    ax2.xaxis.grid(True)
    plt.tick_params('x', labelbottom=False)

    # RSI
    ax3 = plt.subplot(gs[3], sharex=ax0)
    ax3.set_facecolor('#f1faee')
    ax3.yaxis.set_major_formatter(mtick.PercentFormatter())
    plt.plot(stock.index, stock.RSI, color='#ad6eff', label='RSI')
    ax3.legend(loc="upper right")
    plt.xlim([stock.index.min(), stock.index.max()])
    plt.axhline(35, color='#f9989c')
    plt.axhline(80, color='#60e8ad')
    plt.ylim([0, 100])
    plt.tick_params('x', labelbottom=False)
    ax3.grid(visible=True)
    ax3.xaxis.grid(True)
    ax3.yaxis.grid(True)


    # Volume
    ax4 = plt.subplot(gs[4], sharex=ax0)
    plt.bar(stock.index, stock.Volume, label='Volume', color='#b278ff')
    ax4.legend(loc="upper right")
    ax4.set_facecolor('#d8e2dc')
    ax4.xaxis.grid(True)
    plt.show()


def bollinger_bands(stock, std=2):
    # Bollinger band plot with EMA and original historical data
    plt.figure(figsize=(16, 5))
    plt.style.use('seaborn-whitegrid')
    plt.plot(stock.index, stock.Close, color='#3388cf', label='Price')
    plt.plot(stock.index, stock.MA21, color='#ad6eff', label='Moving Average (21 days)')
    # plt.plot(stock.index, stock.MA7, color='#ff6e9d', label='Moving Average (7 days)')
    plt.plot(stock.index, stock.Upper_band, color='#ffbd74', alpha=0.3)
    plt.plot(stock.index, stock.Lower_band, color='#ffa33f', alpha=0.3)
    plt.fill_between(stock.index, stock.Upper_band, stock.Lower_band, color='#ffa33f', alpha=0.1,
                     label='Bollinger Band ({} STD)'.format(std))
    plt.legend(frameon=True, loc=1, ncol=1, borderpad=.6)
    plt.title('Bollinger Bands', fontsize=20)
    plt.ylabel('Price')
    plt.xlim([stock.index.min(), stock.index.max()])
    plt.show()


def volume(stock):
    # Volume plot
    plt.figure(figsize=(16, 2))
    plt.style.use('seaborn-whitegrid')
    plt.title('Volume', fontsize=15)
    plt.ylabel('Volume', fontsize=12)
    plt.plot(stock.index, stock['Volume'].ewm(21).mean())
    plt.xlim([stock.index.min(), stock.index.max()])
    plt.show()


def macd(stock):
    # MACD
    plt.figure(figsize=(16, 2))
    plt.plot(stock.MACD, label='MACD', color='#b278ff')
    plt.plot(stock.Signal, label='Signal', color='#ffa74a')
    plt.axhline(0, color='#557692')
    plt.legend(frameon=True, loc=1, ncol=1, fontsize=10, borderpad=.6)
    plt.title('MACD', fontsize=15)
    plt.ylabel('Strength', fontsize=12)
    plt.show()


def rsi(stock):
    plt.figure(figsize=(16, 5))

    # create an empty grid
    gs = gridspec.GridSpec(2, 1, height_ratios=[2, 1])

    ax1 = plt.subplot(gs[0])
    plt.plot(stock.index, stock.Close, color='#3388cf', label='Price')
    ax1.set_title('RSI', fontsize=12)
    plt.tick_params('x', labelbottom=False)

    ax2 = plt.subplot(gs[1], sharex=ax1)
    ax2.yaxis.set_major_formatter(mtick.PercentFormatter())
    plt.plot(stock.index, stock.RSI, color='#ad6eff')
    plt.tick_params('x', labelbottom=True)
    plt.xlim([stock.index.min(), stock.index.max()])
    plt.axhline(35, color='#f9989c')
    plt.axhline(80, color='#60e8ad')
    # ax2.set_title('RSI', fontsize=8)
    plt.ylim([0, 100])
    plt.show()


def hist(data, name, bins=50):
    plt.rcParams['figure.dpi'] = 227
    plt.figure(figsize=(16, 6))
    plt.style.use('seaborn-whitegrid')
    plt.hist(data, bins=bins)
    plt.title(name, fontsize=16)
    plt.xlabel('Values', fontsize=13)
    plt.ylabel('Quantities', fontsize=13)
    plt.show()


def qqplot(data):
    plt.rcParams['figure.dpi'] = 227
    plt.figure(figsize=(16, 6))
    plt.style.use('seaborn-whitegrid')
    sm.qqplot(data.dropna(), line='s', scale=1)
    plt.title('Check for Normality', fontsize=16)
    plt.show()


def compare_stocks(stocks, value='Close', by='month', scatter=False):
    '''
    Function groups stocks' Close values
    '''
    plt.rcParams['figure.dpi'] = 227
    plt.figure(figsize=(16, 6))
    plt.style.use('seaborn-whitegrid')
    group_by_stock = {}

    for stock in list(stocks.keys()):

        if by == 'month': group_by = stocks[stock].index.month
        if by == 'day': group_by = stocks[stock].index.day
        if by == 'year': group_by = stocks[stock].index.year

        a = stocks[stock].groupby(group_by).mean()[value]
        normalized_price = (a - a.mean()) / a.std()
        group_by_stock[stock] = normalized_price

        if scatter == False:
            plt.plot(normalized_price, label=stock)
        else:
            plt.scatter(normalized_price.keys(), normalized_price.values, label=stock)

    plt.plot(pd.DataFrame(group_by_stock).mean(axis=1), label='ALL', color='black', linewidth=5, linestyle='--')
    plt.legend(frameon=True, fancybox=True, framealpha=.9, loc=1, ncol=4, fontsize=12, title='Stocks')
    plt.title(value + ' by ' + by, fontsize=14)
    plt.xlabel('Period', fontsize=12)
    plt.ylabel(value, fontsize=12)
    plt.show()


def trading_history(stock, net, std=2):
    # Bollinger band plot with EMA and original historical data
    plt.figure(figsize=(16, 5))
    plt.style.use('seaborn-whitegrid')
    plt.plot(stock.index, stock.Close, color='#3388cf', label='Price')
    plt.plot(stock.index, stock.MA21, color='#ad6eff', label='Moving Average (21 days)')
    plt.plot(stock.index, stock.Upper_band, color='#ffbd74', alpha=0.3)
    plt.plot(stock.index, stock.Lower_band, color='#ffa33f', alpha=0.3)
    plt.fill_between(stock.index, stock.Upper_band, stock.Lower_band, color='#ffa33f', alpha=0.1,
                     label='Bollinger Band ({} STD)'.format(std))

    plt.title('Trading History', fontsize=15)
    plt.ylabel('Price', fontsize=12)
    plt.xlim([stock.index.min(), stock.index.max()])

    for i in net:
        if i[2] == 1:
            color = '#ff005e'
        else:
            color = '#4bd81d'
        plt.plot_date(i[0], i[1], color=color)

    plt.plot_date([], [], label='Buy', c='#ff005e')
    plt.plot_date([], [], label='Sell', c='#4bd81d')

    plt.legend(frameon=True, loc=1, ncol=1, fontsize=10, borderpad=.6)
    plt.show()
