import pandas as pd
import datetime as dt

_BBG_URL = 'http://www.bloomberg.com/apps/data?pid=webpxta&Securities={}'
_BBG_TIMEPERIOD = '&TimePeriod=5Y'
_BBG_OUTFIELDS = '&Outfields=HDATE,PR005-H,PR006-H,PR007-H,PR008-H'

def get_stock_feed(ticker, start=None, end=dt.datetime.today()):
    """
    Get historical data for the given ticker from Bloomberg.
    Date format is datetime.
    Order of columns is OHLC.

    Returns a Pandas DataFrame.
    """
    url = _BBG_URL.format(ticker)
    url += _BBG_TIMEPERIOD
    url += _BBG_OUTFIELDS

    # REMINDER: Add options to include BB, MACD, RSI, etc.

    feed = pd.read_csv(url, delimiter='"')
    # Header will mangle the data, so needs to be munged properly.
    feed.drop(feed.columns[[5, 6, 7, 8]], axis=1, inplace=True)
    feed.columns = ['Date', 'Close', 'Open', 'High', 'Low']
    feed = feed[['Date', 'Open', 'High', 'Low', 'Close']].dropna()
    feed.loc[:,'Date'] = pd.to_datetime(feed.loc[:,'Date'])
    feed = _adjust_period(feed, start, end)

    return feed

def _adjust_period(feed, start, end):
    """
    Truncates the stock feed to return only the data desired range.

    Raises an error if provided start date is more than 5 years back. End date
    defaults to today, unless otherwise set.

    Returns a Pandas DataFrame.
    """
    if start is not None:
        if start < feed['Date'].min():
            raise IndexError('Start date cannot be more than 5 years ago.')
        else:
            feed = feed[feed['Date'] >= start]
            feed.reset_index(drop=True, inplace=True)

    feed = feed[feed['Date'] <= end]
    feed.reset_index(drop=True, inplace=True)

    return feed
