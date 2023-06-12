import alpaca_trade_api as tradeapi
import pandas as pd
from timeframe import TimeFrame
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import pandas_market_calendars as mcal
import numpy as np


APCA_API_KEY_ID = 'PKA0XDHFOR2QBKHE7Y7L'
APCA_API_SECRET_KEY = 'r37925RNYTZFUpGewDxaxC1fHwdjHohUojdWBJ0e'
APCA_API_BASE_URL = 'https://paper-api.alpaca.markets'

from alpaca_trade_api.rest import REST, TimeFrame

api = tradeapi.REST(APCA_API_KEY_ID, APCA_API_SECRET_KEY)

def get_daily_notional_value_df(symbol):

    # list for storing daily notional value traded
    daily_notional_value_traded = []

    # list for storing date
    date_index = []

    # generate bars for each minute
    for i in range(1, 100):
        d = timedelta(days=i)
        start_date = (datetime.now() - d).strftime("%Y-%m-%d")
        end_date = (datetime.now() - d).strftime("%Y-%m-%d")
        trades_df = api.get_bars(symbol, TimeFrame.Minute, start_date, end_date, adjustment='all').df
        trades_df['notional value traded'] = ""
        # calculate notional traded values for each day and add to list
        for j in trades_df.index:
            trades_df['notional value traded'] = trades_df['volume'] * trades_df['vwap']
        daily_notional_value_traded.append(trades_df['notional value traded'].sum())
        date_index.append(start_date)

    # convert list to dataframe
    daily_not_val_traded_df = pd.DataFrame(daily_notional_value_traded, columns = ['daily_notional_value_traded'])
    date_df = pd.DataFrame(date_index, columns = ['date'])
    daily_not_val_traded_df = pd.concat([date_df, daily_not_val_traded_df], axis=1)
    daily_not_val_traded_df = daily_not_val_traded_df[daily_not_val_traded_df.daily_notional_value_traded != 0]
    daily_not_val_traded_df = daily_not_val_traded_df.set_index('date')
    return daily_not_val_traded_df

def SMA_10(daily_not_val_traded_df):
    # calculating moving average
    daily_not_val_traded_df['SMA10'] = daily_not_val_traded_df['daily_notional_value_traded'].rolling(10).mean()
    daily_not_val_traded_df.dropna(inplace=True)

def get_minute_bars_df(symbol):
    # generate bars for each minute
    d1 = timedelta(days=100)
    d2 = timedelta(days=1)
    start_date = (datetime.now() - d1).strftime("%Y-%m-%d")
    end_date = (datetime.now() - d2).strftime("%Y-%m-%d")
    trades_df = api.get_bars(symbol, TimeFrame.Minute, start_date, end_date, adjustment='all').df
    trades_df['date'] = ""
    for i in trades_df.index:
        trades_df.at[i, 'date'] = i.strftime("%Y-%m-%d")
    return trades_df

def merge_SMA_trade_normalize(trades_df, daily_not_val_traded_df):
    # merge SMA and trade dataframes
    trades_df = trades_df.merge(daily_not_val_traded_df, on='date')
    trades_df = trades_df.set_index('date')

    # calculate normalized notional value traded
    trades_df['normalized_notional_value_traded'] = trades_df['volume'] * trades_df['vwap'] / trades_df['SMA10']
    return trades_df

def filter_large_trades(trades_df):
    # sort dataframe by date into a dataframe list for each day
    DFList = []
    for group in trades_df.groupby(trades_df.index):
        DFList.append(group[1])
    # calculating 99.9 percentile and filtering values that are in that percentile
    filtered = []
    index = 0
    for i in DFList:
        border = i['normalized_notional_value_traded'].quantile(0.999)
        filtered.append(i[i['normalized_notional_value_traded'] > border])
        index += 1
    return filtered

def get_filtered_trade_EMA(filtered):
    # creating exponential moving average for large trades
    ewm = 5

    filtered_df = pd.concat(filtered)
    filtered_df['EMA'] = filtered_df['normalized_notional_value_traded'].ewm(span=int(ewm), adjust=False).mean()
    return filtered_df

def get_large_trades_json(filtered_df, trades_df):
    # tool for filtering large trades in data
    new = filtered_df.drop(['open', 'high', 'low', 'close', 'volume', 'trade_count', 'vwap', 'daily_notional_value_traded', 'SMA10', 'normalized_notional_value_traded'], axis=1)
    
    trades_df = trades_df.merge(new, on='date')
    trades_df = trades_df[trades_df.normalized_notional_value_traded >= trades_df.EMA]
    trades_df = trades_df.drop(['high', 'low','daily_notional_value_traded', 'SMA10', 'normalized_notional_value_traded'], axis=1)
    trades_df = trades_df.reset_index()
    return trades_df.to_json(), trades_df.to_csv('current.csv', encoding='utf-8')

def get_large_trades(symbol):
    symbol = str.lower(symbol)
    print(symbol)
    daily_not_val_traded_df = get_daily_notional_value_df(symbol)
    SMA_10(daily_not_val_traded_df)
    trades_df = get_minute_bars_df(symbol)
    trades_df = merge_SMA_trade_normalize(trades_df, daily_not_val_traded_df)
    filtered = filter_large_trades(trades_df)
    filtered_df = get_filtered_trade_EMA(filtered)
    return get_large_trades_json(filtered_df, trades_df)