from common import *

def TSD(df: pd.DataFrame, channel_lenght=10, average_lenght=21, mfiperiod=58):
    """
    Returns a dataframe with:
    'tsd_value': the value of the indicator. A large negative value indicates a buy. Typically, -53 is a good threshold.
    'mfi_value': The modified MFI value for the indicator. This is not the typical MFI but a derivative. Typically, a buy signal 
    from the tsd_value with a negative MFI has more weight. Sell signals are the opposite.
    'green': A boolean field depicting a green dot if True, and red if false.

    The input dataframe needs to be in OHLCV format with lowercase fields.
    """
    ap = (df.high + df.low + df.close)/3
    esa = ta.EMA(ap, timeperiod=channel_lenght)
    d = ta.EMA(np.abs(ap - esa), timeperiod=channel_lenght)
    ci = (ap - esa) /  (0.015 * d)
    tci = ta.EMA(ci, timeperiod=average_lenght)
    wt1 = pd.Series(tci)
    wt2 = pd.Series(ta.SMA(wt1, timeperiod=4))

    mf = ta.MFI(df.high, df.low, df.close, df.volume, mfiperiod)
    mfi = (mf - 50) * 3

    a = crossed_above(wt1, wt2)
    b = crossed_below(wt1, wt2)
    green = np.where(wt1 >= wt2, True, False)

    r = np.where(a | b, wt2, 0)

    return pd.DataFrame(index=df.index, data={
        'tsd_value': r,
        'mfi_value': mfi,
        'green': green
    })