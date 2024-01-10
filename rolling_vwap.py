from common import *

def rolling_vwap(df, window=10):
    """
    Returns a pandas series with the Rolling VWAP according to the window value passed, which defaults to 10 periods.
    The input dataframe needs to be in OHLCV format with lowercase fields.
    """
    # Calculate HLC3 (High, Low, Close average)
    hlc3 = (df['high'] + df['low'] + df['close']) / 3

    # Calculate rolling VWAP using HLC3
    vwap = (hlc3 * df['volume']).rolling(window=window).sum() / df['volume'].rolling(window=window).sum()
    return vwap