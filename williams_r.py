from common import *

def williams_r(dataframe: pd.DataFrame, period: int = 21, ema: int = 13) -> pd.Series:
    """
    Williams %R is a technical analysis oscillator showing the current closing price in relation to the high and low
    of the past N days (for a given N). It was developed by Larry Williams.
    The oscillator is on a negative scale, from -100 (lowest) up to 0 (highest).
    It returns two Pandas series, one with the %R value per se, and the other one with its EMA value.
    """

    highest_high = dataframe["high"].rolling(center=False, window=period).max()
    lowest_low = dataframe["low"].rolling(center=False, window=period).min()

    WR = pd.Series(
        (highest_high - dataframe["close"]) / (highest_high - lowest_low) * -100,
        name=f"{period} Williams %R",
        )

    # Apply EMA to the scaled Williams %R
    e = pd.Series(ta.EMA(WR, timeperiod=ema), name=f"{ema} period EMA of Williams %R")

    return WR, e