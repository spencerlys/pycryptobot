"""Plots (and/or saves) the graphical trading data using Matplotlib"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import datetime, re, sys

from models.Trading import TechnicalAnalysis
from models.helper.LogHelper import Logger
from models.PyCryptoBot import PyCryptoBot

sys.path.append('.')

class TradingGraphs():
    def __init__(self, technical_analysis):
        """Trading Graphs object model

        Parameters
        ----------
        technical_analysis : object
            TechnicalAnalysis object to provide the trading data to visualise
        """

        # validates the technical_analysis object
        if not isinstance(technical_analysis, TechnicalAnalysis):
            raise TypeError('Coinbase Pro model required.')

        # only one figure can be open at a time, close all open figures
        plt.close('all')

        self.technical_analysis = technical_analysis

        # stores the pandas dataframe from technical_analysis object
        self.df = technical_analysis.getDataFrame()

        # stores the support and resistance levels from technical_analysis object
        self.levels = technical_analysis.getSupportResistanceLevels()

        # set graph format
        plt.style.use('seaborn')

    def renderBuySellSignalEMA1226(self, saveFile='', saveOnly=False):
        """Render the EMA12 and EMA26 buy and sell signals

        Parameters
        ----------
        saveFile : str, optional
            Save the figure
        saveOnly : bool
            Save the figure without displaying it
        """

        buysignals = self.df[self.df.ema12gtema26co is True]
        sellsignals = self.df[self.df.ema12ltema26co is True]

        plt.subplot(111)
        plt.plot(self.df.close, label="price", color="royalblue")
        plt.plot(self.df.ema12, label="ema12", color="orange")
        plt.plot(self.df.ema26, label="ema26", color="purple")
        plt.ylabel('Price')

        for idx in buysignals.index.tolist():
            plt.axvline(x=idx, color='green')

        for idx in sellsignals.index.tolist():
            plt.axvline(x=idx, color='red')

        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.legend()

        try:
            if saveFile != '':
                plt.savefig(saveFile)
        except OSError:
            raise SystemExit('Unable to save: ', saveFile)

        if saveOnly is False:
            plt.show()

    def renderBuySellSignalEMA1226MACD(self, saveFile='', saveOnly=False):
        """Render the EMA12, EMA26 and MACD buy and sell signals

        Parameters
        ----------
        saveFile : str, optional
            Save the figure
        saveOnly : bool
            Save the figure without displaying it
        """

        buysignals = ((self.df.ema12gtema26co is True) & (self.df.macdgtsignal is True) & (self.df.goldencross is True))
        sellsignals = ((self.df.ema12ltema26co is True) & (self.df.macdltsignal is True))
        df_signals = self.df[(buysignals) | (sellsignals)]

        ax1 = plt.subplot(211)
        plt.plot(self.df.close, label="price", color="royalblue")
        plt.plot(self.df.ema12, label="ema12", color="orange")
        plt.plot(self.df.ema26, label="ema26", color="purple")
        plt.ylabel('Price')

        action = ''
        last_action = ''
        for idx, row in df_signals.iterrows():
            if row['ema12gtema26co'] is True and row['macdgtsignal'] is True and last_action != 'buy':
                action = 'buy'
                plt.axvline(x=idx, color='green')
            elif row['ema12ltema26'] is True and row['macdltsignal'] is True and action == 'buy':
                action = 'sell'
                plt.axvline(x=idx, color='red')

            last_action = action

        plt.xticks(rotation=90)

        plt.subplot(212, sharex=ax1)
        plt.plot(self.df.macd, label="macd")
        plt.plot(self.df.signal, label="signal")
        plt.legend()
        plt.ylabel('Divergence')
        plt.xticks(rotation=90)

        plt.tight_layout()
        plt.legend()

        try:
            if saveFile != '':
                plt.savefig(saveFile)
        except OSError:
            raise SystemExit('Unable to save: ', saveFile)

        if saveOnly is False:
            plt.show()

    def renderFibonacciBollingerBands(self, period=50, saveFile='', saveOnly=False):
        """Render FibonacciBollingerBands"""

        if not isinstance(period, int):
            raise TypeError('Period parameter is not perioderic.')

        if period < 1 or period > len(self.df):
            raise ValueError('Period is out of range')

        df_subset = self.df.iloc[-period::]

        plt.subplot(111)
        plt.suptitle(df_subset.iloc[0]['market'] + ' | ' + str(df_subset.iloc[0]['granularity']), fontsize=12)
        plt.plot(df_subset.fbb_upper0_236, label="23.6%", color="blue")
        plt.plot(df_subset.fbb_lower0_236, label="-23.6%", color="blue")
        plt.plot(df_subset.fbb_upper0_382, label="38.2%", color="green")
        plt.plot(df_subset.fbb_lower0_382, label="3-8.2%", color="green")
        plt.plot(df_subset.fbb_upper0_5, label="50%", color="cyan")
        plt.plot(df_subset.fbb_lower0_5, label="-50%", color="cyan")
        plt.plot(df_subset.fbb_upper0_618, label="61.8%", color="pink")
        plt.plot(df_subset.fbb_lower0_618, label="-61.8%", color="pink")
        plt.plot(df_subset.fbb_upper0_764, label="76.4%", color="red")
        plt.plot(df_subset.fbb_lower0_764, label="-76.4%", color="red")
        plt.plot(df_subset.fbb_upper1, label="100%", color="magenta")
        plt.plot(df_subset.fbb_lower1, label="-100%", color="magenta")
        plt.plot(df_subset.fbb_mid, label="mid", color="orange")
        plt.plot(df_subset.close, label="price", color="black")
        plt.legend()
        plt.ylabel('Price')
        plt.xticks(rotation=90)
        plt.tight_layout()

        try:
            if saveFile != '':
                plt.savefig(saveFile)
        except OSError:
            raise SystemExit('Unable to save: ', saveFile)

        if saveOnly is False:
            plt.show()

    def renderPriceEMA12EMA26(self, saveFile='', saveOnly=False):
        """Render the price, EMA12 and EMA26

        Parameters
        ----------
        saveFile : str, optional
            Save the figure
        saveOnly : bool
            Save the figure without displaying it
        """

        plt.subplot(111)
        plt.plot(self.df.close, label="price")
        plt.plot(self.df.ema12, label="ema12")
        plt.plot(self.df.ema26, label="ema26")
        plt.legend()
        plt.ylabel('Price')
        plt.xticks(rotation=90)
        plt.tight_layout()

        try:
            if saveFile != '':
                plt.savefig(saveFile)
        except OSError:
            raise SystemExit('Unable to save: ', saveFile)

        if saveOnly is False:
            plt.show()

    def renderEMAandMACD(self, period=30, saveFile='', saveOnly=False):
        """Render the price, EMA12, EMA26 and MACD

        Parameters
        ----------
        saveFile : str, optional
            Save the figure
        saveOnly : bool
            Save the figure without displaying it
        """

        if not isinstance(period, int):
            raise TypeError('Period parameter is not perioderic.')

        if period < 1 or period > len(self.df):
            raise ValueError('Period is out of range')

        df_subset = self.df.iloc[-period::]

        date = pd.to_datetime(df_subset.index).to_pydatetime()

        df_subset_length = len(df_subset)
        indices = np.arange(df_subset_length) # the evenly spaced plot indices

        def format_date(x, pos=None): #pylint: disable=unused-argument
            thisind = np.clip(int(x + 0.5), 0, df_subset_length - 1)
            return date[thisind].strftime('%Y-%m-%d %H:%M:%S')

        fig, (ax1, ax2) = plt.subplots(nrows=2, figsize=(12, 6))
        fig.suptitle(df_subset.iloc[0]['market'] + ' | ' + str(df_subset.iloc[0]['granularity']), fontsize=16)
        plt.xticks(rotation=90)
        #plt.tight_layout()

        indices = np.arange(len(df_subset))

        ax1.plot(indices, df_subset['close'], label='price', color='royalblue')
        ax1.plot(indices, df_subset['ema12'], label='ema12', color='orange')
        ax1.plot(indices, df_subset['ema26'], label='ema26', color='purple')
        ax1.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
        ax1.set_title('Price, EMA12 and EMA26')
        ax1.set_ylabel('Price')
        ax1.legend()
        fig.autofmt_xdate()

        ax2.plot(indices, df_subset.macd, label='macd')
        ax2.plot(indices, df_subset.signal, label='signal')
        ax2.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
        ax2.set_title('MACD')
        ax2.set_ylabel('Divergence')
        ax2.legend()
        fig.autofmt_xdate()

        try:
            if saveFile != '':
                plt.savefig(saveFile)
        except OSError:
            raise SystemExit('Unable to save: ', saveFile)

        if saveOnly is False:
            plt.show()

    def renderSeasonalARIMAModel(self, saveFile='', saveOnly=False):
        """Render the seasonal ARIMA model

        Parameters
        ----------
        saveFile : str, optional
            Save the figure
        saveOnly : bool
            Save the figure without displaying it
        """

        fittedValues = self.technical_analysis.seasonalARIMAModelFittedValues()

        plt.plot(self.df['close'], label='original')
        plt.plot(fittedValues, color='red', label='fitted')
        plt.title('RSS: %.4f' % sum((fittedValues-self.df['close'])**2))
        plt.legend()
        plt.ylabel('Price')
        plt.xticks(rotation=90)
        plt.tight_layout()

        try:
            if saveFile != '':
                plt.savefig(saveFile)
        except OSError:
            raise SystemExit('Unable to save: ', saveFile)

        if saveOnly is False:
            plt.show()

    def renderSMAandMACD(self, saveFile='', saveOnly=False):
        """Render the price, SMA20, SMA50, and SMA200

        Parameters
        ----------
        saveFile : str, optional
            Save the figure
        saveOnly : bool
            Save the figure without displaying it
        """

        ax1 = plt.subplot(211)
        plt.plot(self.df.close, label="price")
        plt.plot(self.df.sma20, label="sma20")
        plt.plot(self.df.sma50, label="sma50")
        plt.plot(self.df.sma200, label="sma200")
        plt.legend()
        plt.ylabel('Price')
        plt.xticks(rotation=90)
        plt.subplot(212, sharex=ax1)
        plt.plot(self.df.macd, label="macd")
        plt.plot(self.df.signal, label="signal")
        plt.legend()
        plt.ylabel('Price')
        plt.xlabel('Days')
        plt.xticks(rotation=90)
        plt.tight_layout()

        try:
            if saveFile != '':
                plt.savefig(saveFile)
        except OSError:
            raise SystemExit('Unable to save: ', saveFile)

        if saveOnly is False:
            plt.show()


    def renderSeasonalARIMAModelPrediction(self, days=30, saveOnly=False):
        """Render the seasonal ARIMA model prediction

        Parameters
        ----------
        days     : int
            Number of days to predict
        saveOnly : bool
            Save the figure without displaying it
        """

        # get dataframe from technical analysis object
        df = self.technical_analysis.getDataFrame()

        if not isinstance(days, int):
            raise TypeError('Prediction days is not numeric.')

        if days < 1 or days > len(df):
            raise ValueError('Predication days is out of range')

        # extract market and granularity from trading dataframe
        market = df.iloc[0].market
        granularity = df.iloc[0].granularity

        results_ARIMA = self.technical_analysis.seasonalARIMAModel()
        df = pd.DataFrame(self.df['close'])
        start_date = df.last_valid_index()
        end_date = start_date + datetime.timedelta(days=days)
        print(start_date)
        print(end_date)
        pred = results_ARIMA.predict(start=str(start_date), end=str(end_date), dynamic=True)

        fig, axes = plt.subplots(ncols=1, figsize=(12, 6)) #pylint: disable=unused-variable
        fig.autofmt_xdate()
        ax1 = plt.subplot(111)
        ax1.set_title('Seasonal ARIMA Model Prediction')

        date = pd.to_datetime(pred.index).to_pydatetime()

        pred_length = len(pred)
        # the evenly spaced plot indices
        indices = np.arange(pred_length) #pylint: disable=unused-variable

        def format_date(x, pos=None): #pylint: disable=unused-argument
            thisind = np.clip(int(x + 0.5), 0, pred_length - 1)
            return date[thisind].strftime('%Y-%m-%d %H:%M:%S')

        fig, ax = plt.subplots(ncols=1, figsize=(12, 6)) #pylint: disable=unused-variable
        fig.autofmt_xdate()

        ax = plt.subplot(111)
        ax.set_title('Seasonal ARIMA Model Prediction')
        ax.plot(pred, label='prediction', color='black')
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))

        plt.xticks(rotation=90)
        plt.tight_layout()

        try:
            Logger.info('creating: graphs/SAM_' + market + '_' + str(granularity) + '.png')
            plt.savefig('graphs/SAM_' + market + '_' + str(granularity) + '.png', dpi=300)
        except OSError:
            raise SystemExit('Unable to save: graphs/SAM_' + market + '_' + str(granularity) + '.png')

        if saveOnly is False:
            plt.show()

    def renderCandlestickAstralPattern(self, period=30, saveOnly=False):
        # get dataframe from technical analysis object
        df = self.technical_analysis.getDataFrame()

        if not isinstance(period, int):
            raise TypeError('Period parameter is not perioderic.')

        if period < 1 or period > len(df):
            raise ValueError('Period is out of range')

        # extract market and granularity from trading dataframe
        market = df.iloc[0].market
        granularity = df.iloc[0].granularity

        df_subset = df.iloc[-period::]

        fig, axes = plt.subplots(ncols=1, figsize=(12, 6)) #pylint: disable=unused-variable
        fig.autofmt_xdate()
        ax1 = plt.subplot(111)
        ax1.set_title('Astral Candlestick Pattern')
        plt.plot(df_subset['close'], label='price', color='black')
        plt.plot(df_subset['ema12'], label='ema12', color='orange')
        plt.plot(df_subset['ema26'], label='ema26', color='purple')
        plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)

        df_candlestick = self.df[self.df['astral_buy'] is True]
        df_candlestick_in_range = df_candlestick[df_candlestick.index >= np.min(df_subset.index)]
        for idx in df_candlestick_in_range.index.tolist():
            plt.plot(idx, df_candlestick_in_range.loc[idx]['close'], 'g^', markersize=8)

        df_candlestick = self.df[self.df['astral_sell'] is True]
        df_candlestick_in_range = df_candlestick[df_candlestick.index >= np.min(df_subset.index)]
        for idx in df_candlestick_in_range.index.tolist():
            plt.plot(idx, df_candlestick_in_range.loc[idx]['close'], 'rv', markersize=8)

        plt.xlabel(market + ' - ' + str(granularity))
        plt.ylabel('Price')
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.legend()

        try:
            Logger.info('creating: graphs/CAP_' + market + '_' + str(granularity) + '.png')
            plt.savefig('graphs/CAP_' + market + '_' + str(granularity) + '.png', dpi=300)
        except OSError:
            raise SystemExit('Unable to save: graphs/CAP_' + market + '_' + str(granularity) + '.png')

        if saveOnly is False:
            plt.show()

    def renderCandlesticks(self, period=30, saveOnly=False):
        # get dataframe from technical analysis object
        df = self.technical_analysis.getDataFrame()

        if not isinstance(period, int):
            raise TypeError('Period parameter is not perioderic.')

        if period < 1 or period > len(df):
            raise ValueError('Period is out of range')

        # extract market and granularity from trading dataframe
        market = df.iloc[0].market
        granularity = df.iloc[0].granularity

        df_subset = df.iloc[-period::]

        fig, axes = plt.subplots(ncols=1, figsize=(12, 6)) #pylint: disable=unused-variable
        fig.autofmt_xdate()
        ax1 = plt.subplot(111)
        ax1.set_title('Candlestick Patterns')
        plt.plot(df_subset['close'], label='price', color='black')
        plt.plot(df_subset['ema12'], label='ema12', color='orange')
        plt.plot(df_subset['ema26'], label='ema26', color='purple')
        plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)

        print(df_subset)
        print(self.df)

        candleCount = 0

        df_candlestick = self.df[self.df['three_white_soldiers'] == True]
        df_candlestick_in_range = df_candlestick[df_candlestick.index >= np.min(df_subset.index)]
        for idx in df_candlestick_in_range.index.tolist():
            if candleCount == 0:
                plt.plot(idx, df_candlestick_in_range.loc[idx]['close'], 'g*', markersize=10, label='Three White Soldiers')
            else:
                plt.plot(idx, df_candlestick_in_range.loc[idx]['close'], 'g*', markersize=10)
            candleCount += 1

        candleCount = 0
        df_candlestick = self.df[self.df['three_black_crows'] == True]
        df_candlestick_in_range = df_candlestick[df_candlestick.index >= np.min(df_subset.index)]
        for idx in df_candlestick_in_range.index.tolist():
            if candleCount == 0:
                plt.plot(idx, df_candlestick_in_range.loc[idx]['close'], 'r*', markersize=10, label='Three Black Crows')
            else:
                plt.plot(idx, df_candlestick_in_range.loc[idx]['close'], 'r*', markersize=10)
            candleCount += 1

        candleCount = 0
        df_candlestick = self.df[self.df['inverted_hammer'] == True]
        df_candlestick_in_range = df_candlestick[df_candlestick.index >= np.min(df_subset.index)]
        for idx in df_candlestick_in_range.index.tolist():
            if candleCount == 0:
                plt.plot(idx, df_candlestick_in_range.loc[idx]['close'], 'y*', markersize=10, label='Inverted Hammer')
            else:
                plt.plot(idx, df_candlestick_in_range.loc[idx]['close'], 'y*', markersize=10)
            candleCount += 1

        candleCount = 0
        df_candlestick = self.df[self.df['hammer'] == True]
        df_candlestick_in_range = df_candlestick[df_candlestick.index >= np.min(df_subset.index)]
        for idx in df_candlestick_in_range.index.tolist():
            if candleCount == 0:
                plt.plot(idx, df_candlestick_in_range.loc[idx]['close'], 'c*', markersize=10, label='Hammer')
            else:
                plt.plot(idx, df_candlestick_in_range.loc[idx]['close'], 'c*', markersize=10)
            candleCount += 1

        candleCount = 0
        df_candlestick = self.df[self.df['hanging_man'] == True]
        df_candlestick_in_range = df_candlestick[df_candlestick.index >= np.min(df_subset.index)]
        for idx in df_candlestick_in_range.index.tolist():
            if candleCount == 0:
                plt.plot(idx, df_candlestick_in_range.loc[idx]['close'], 'm*', markersize=10, label='Hanging Man')
            else:
                plt.plot(idx, df_candlestick_in_range.loc[idx]['close'], 'm*', markersize=10)
            candleCount += 1

        candleCount = 0
        df_candlestick = self.df[self.df['shooting_star'] == True]
        df_candlestick_in_range = df_candlestick[df_candlestick.index >= np.min(df_subset.index)]
        for idx in df_candlestick_in_range.index.tolist():
            if candleCount == 0:
                plt.plot(idx, df_candlestick_in_range.loc[idx]['close'], 'k*', markersize=10, label='Shooting Star')
            else:
                plt.plot(idx, df_candlestick_in_range.loc[idx]['close'], 'k*', markersize=10)
            candleCount += 1

        candleCount = 0
        df_candlestick = self.df[self.df['doji'] == True]
        df_candlestick_in_range = df_candlestick[df_candlestick.index >= np.min(df_subset.index)]
        for idx in df_candlestick_in_range.index.tolist():
            if candleCount == 0:
                plt.plot(idx, df_candlestick_in_range.loc[idx]['close'], 'b*', markersize=10, label='Doji')
            else:
                plt.plot(idx, df_candlestick_in_range.loc[idx]['close'], 'b*', markersize=10)
            candleCount += 1

        candleCount = 0
        df_candlestick = self.df[self.df['three_line_strike'] == True]
        df_candlestick_in_range = df_candlestick[df_candlestick.index >= np.min(df_subset.index)]
        for idx in df_candlestick_in_range.index.tolist():
            if candleCount == 0:
                plt.plot(idx, df_candlestick_in_range.loc[idx]['close'], 'g*', markersize=10, label='Three Line Strike')
            else:
                plt.plot(idx, df_candlestick_in_range.loc[idx]['close'], 'g*', markersize=10)
            candleCount += 1

        candleCount = 0
        df_candlestick = self.df[self.df['two_black_gapping'] == True]
        df_candlestick_in_range = df_candlestick[df_candlestick.index >= np.min(df_subset.index)]
        for idx in df_candlestick_in_range.index.tolist():
            if candleCount == 0:
                plt.plot(idx, df_candlestick_in_range.loc[idx]['close'], 'r*', markersize=10, label='Two Black Gapping')
            else:
                plt.plot(idx, df_candlestick_in_range.loc[idx]['close'], 'r*', markersize=10)
            candleCount += 1

        candleCount = 0
        df_candlestick = self.df[self.df['morning_star'] == True]
        df_candlestick_in_range = df_candlestick[df_candlestick.index >= np.min(df_subset.index)]
        for idx in df_candlestick_in_range.index.tolist():
            if candleCount == 0:
                plt.plot(idx, df_candlestick_in_range.loc[idx]['close'], 'g*', markersize=10, label='Morning Star')
            else:
                plt.plot(idx, df_candlestick_in_range.loc[idx]['close'], 'g*', markersize=10)
            candleCount += 1

        candleCount = 0
        df_candlestick = self.df[self.df['evening_star'] == True]
        df_candlestick_in_range = df_candlestick[df_candlestick.index >= np.min(df_subset.index)]
        for idx in df_candlestick_in_range.index.tolist():
            if candleCount == 0:
                plt.plot(idx, df_candlestick_in_range.loc[idx]['close'], 'r*', markersize=10, label='Evening Star')
            else:
                plt.plot(idx, df_candlestick_in_range.loc[idx]['close'], 'r*', markersize=10)
            candleCount += 1

        candleCount = 0
        df_candlestick = self.df[self.df['morning_doji_star'] == True]
        df_candlestick_in_range = df_candlestick[df_candlestick.index >= np.min(df_subset.index)]
        for idx in df_candlestick_in_range.index.tolist():
            if candleCount == 0:
                plt.plot(idx, df_candlestick_in_range.loc[idx]['close'], 'g*', markersize=10, label='Morning Doji Star')
            else:
                plt.plot(idx, df_candlestick_in_range.loc[idx]['close'], 'g*', markersize=10)
            candleCount += 1

        candleCount = 0
        df_candlestick = self.df[self.df['evening_doji_star'] == True]
        df_candlestick_in_range = df_candlestick[df_candlestick.index >= np.min(df_subset.index)]
        for idx in df_candlestick_in_range.index.tolist():
            if candleCount == 0:
                plt.plot(idx, df_candlestick_in_range.loc[idx]['close'], 'r*', markersize=10, label='Evening Doji Star')
            else:
                plt.plot(idx, df_candlestick_in_range.loc[idx]['close'], 'r*', markersize=10)
            candleCount += 1

        candleCount = 0
        df_candlestick = self.df[self.df['abandoned_baby'] == True]
        df_candlestick_in_range = df_candlestick[df_candlestick.index >= np.min(df_subset.index)]
        for idx in df_candlestick_in_range.index.tolist():
            if candleCount == 0:
                plt.plot(idx, df_candlestick_in_range.loc[idx]['close'], 'g*', markersize=10, label='Abandoned Baby')
            else:
                plt.plot(idx, df_candlestick_in_range.loc[idx]['close'], 'g*', markersize=10)
            candleCount += 1

        plt.xlabel(market + ' - ' + str(granularity))
        plt.ylabel('Price')
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.legend()

        try:
            Logger.info('creating: graphs/CSP_' + market + '_' + str(granularity) + '.png')
            plt.savefig('graphs/CSP_' + market + '_' + str(granularity) + '.png', dpi=300)
            PyCryptoBot().docTelegram(market + '_' + str(granularity) + ' 蜡烛线分析', 'graphs/CSP_' + market + '_' + str(granularity) + '.png')
        except OSError:
            raise SystemExit('Unable to save: graphs/CSP_' + market + '_' + str(granularity) + '.png')

        if saveOnly is False:
            plt.show()

    def renderFibonacciRetracement(self, saveOnly=False):
        """Render Fibonacci Retracement Levels

        Parameters
        ----------
        saveOnly : bool
            Save the figure without displaying it
        """

        # get dataframe from technical analysis object
        df = self.technical_analysis.getDataFrame()

        # extract market and granularity from trading dataframe
        market = df.iloc[0].market
        granularity = df.iloc[0].granularity

        # closing price min and max values
        price_min = df.close.min()
        price_max = df.close.max()

        # fibonacci retracement levels
        diff = price_max - price_min
        level1 = price_max - 0.236 * diff
        level2 = price_max - 0.382 * diff
        level3 = price_max - 0.618 * diff

        fig, ax = plt.subplots(ncols=1, figsize=(12, 6)) #pylint: disable=unused-variable
        fig.autofmt_xdate()

        ax = plt.subplot(111)
        ax.plot(df.close, label='price', color='black')
        ax.set_title('Fibonacci Retracement Levels')
        ax.axhspan(level1, price_min, alpha=0.4, color='lightsalmon', label='0.618')
        ax.axhspan(level3, level2, alpha=0.5, color='palegreen', label='0.382')
        ax.axhspan(level2, level1, alpha=0.5, color='palegoldenrod', label='0.236')
        ax.axhspan(price_max, level3, alpha=0.5, color='powderblue', label='0')

        plt.xlabel(market + ' - ' + str(granularity))
        plt.ylabel('Price')
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.legend()

        try:
            Logger.info('creating: graphs/FRL_' + market + '_' + str(granularity) + '.png')
            plt.savefig('graphs/FRL_' + market + '_' + str(granularity) + '.png', dpi=300)
            PyCryptoBot().docTelegram(market + '_' + str(granularity) + ' 斐波那契数列', 'graphs/FRL_' + market + '_' + str(granularity) + '.png')
        except OSError:
            raise SystemExit('Unable to save: graphs/FRL_' + market + '_' + str(granularity) + '.png')

        if saveOnly is False:
            plt.show()

    def renderSupportResistance(self, saveOnly=False):
        """Render Support and Resistance Levels

        Parameters
        ----------
        saveOnly : bool
            Save the figure without displaying it
        """

        # get dataframe from technical analysis object
        df = self.technical_analysis.getDataFrame()

        # extract market and granularity from trading dataframe
        market = df.iloc[0].market
        granularity = df.iloc[0].granularity

        fig, ax = plt.subplots(ncols=1, figsize=(12, 6)) #pylint: disable=unused-variable
        fig.autofmt_xdate()

        ax = plt.subplot(111)
        ax.plot(df.close, label='price', color='black')
        ax.set_title('Support and Resistance Levels')

        rotation = 1
        last_level = 0
        for level in self.levels:
            #plt.axhline(y=level, color='grey')
            if last_level != 0:
                if rotation == 1:
                    ax.axhspan(last_level, level, alpha=0.4, color='lightsalmon', label=str(level))
                elif rotation == 2:
                    ax.axhspan(last_level, level, alpha=0.5, color='palegreen', label=str(level))
                elif rotation == 3:
                    ax.axhspan(last_level, level, alpha=0.5, color='palegoldenrod', label=str(level))
                elif rotation == 4:
                    ax.axhspan(last_level, level, alpha=0.5, color='powderblue', label=str(level))
                else:
                    ax.axhspan(last_level, level, alpha=0.4)
            last_level = level
            if rotation < 4:
                rotation += 1
            else:
                rotation = 1

        plt.xlabel(market + ' - ' + str(granularity))
        plt.ylabel('Price')
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.legend()

        try:
            Logger.info('creating: graphs/SRL_' + market + '_' + str(granularity) + '.png')
            plt.savefig('graphs/SRL_' + market + '_' + str(granularity) + '.png', dpi=300)
            PyCryptoBot().docTelegram(market + '_' + str(granularity) + ' 支撑与压力位', 'graphs/SRL_' + market + '_' + str(granularity) + '.png')
        except OSError:
            raise SystemExit('Unable to save: graphs/SRL_' + market + '_' + str(granularity) + '.png')

        if saveOnly is False:
            plt.show()

    def renderPercentageChangeHistogram(self, show_desc=True):
        """Render Percentage Change Histogram

        Parameters
        ----------
        saveOnly : bool
            Save the figure without displaying it
        """

        # get dataframe from technical analysis object
        df = self.technical_analysis.getDataFrame()

        # extract market and granularity from trading dataframe
        market = df.iloc[0].market
        granularity = df.iloc[0].granularity

        fig, ax = plt.subplots(ncols=1, figsize=(12, 6)) #pylint: disable=unused-variable
        fig.autofmt_xdate()

        ax = plt.subplot(111)
        df.close_pc.hist(bins=50)
        ax.set_title('Close Percent Change')

        plt.xlabel(market + ' - ' + str(granularity))
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.legend()

        plt.show()

        if show_desc is True:
            Logger.info(df['close_pc'].describe())

    def renderPercentageChangeScatterMatrix(self):
        """Render Percentage Change Scatter Matrix

        Parameters
        ----------
        saveOnly : bool
            Save the figure without displaying it
        """

        # get dataframe from technical analysis object
        df = self.technical_analysis.getDataFrame()

        pd.plotting.scatter_matrix(df[['close','close_pc','close_cpc']], diagonal='kde', alpha=0.1, figsize=(12,12))
        plt.tight_layout()
        plt.show()

    def renderCumulativeReturn(self):
        """Render Percentage Change Histogram

        Parameters
        ----------
        saveOnly : bool
            Save the figure without displaying it
        """

        # get dataframe from technical analysis object
        df = self.technical_analysis.getDataFrame()

        # extract market and granularity from trading dataframe
        market = df.iloc[0].market
        granularity = df.iloc[0].granularity

        fig, ax = plt.subplots(ncols=1, figsize=(12, 6)) #pylint: disable=unused-variable
        fig.autofmt_xdate()

        ax = plt.subplot(111)
        ax.plot(df.close_cpc, label='Adj Close', color='black')
        ax.set_title('Cumulative Return')

        plt.xlabel(market + ' - ' + str(granularity))
        plt.ylabel('Return')
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.legend()

        plt.show()
