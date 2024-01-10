from common import *
import math

def FRAMA(df, src='Close', len=20, FC=1, SC=200):
    """ 
    Returns the FRAMA moving average. 
    The input dataframe needs to be in OHLCV format with lowercase fields.
    """
    len1 = len // 2
    e = math.e
    w = math.log(2 / (SC + 1)) / math.log(e)
    H1 = ta.MAX(df['high'].values, timeperiod=len1)
    L1 = ta.MIN(df['low'].values, timeperiod=len1)
    N1 = (H1 - L1) / len1
    H2 = ta.MAX(df['high'].shift(len1).values, timeperiod=len1)
    L2 = ta.MIN(df['low'].shift(len1).values, timeperiod=len1)
    N2 = (H2 - L2) / len1
    H3 = ta.MAX(df['high'].values, timeperiod=len)
    L3 = ta.MIN(df['low'].values, timeperiod=len)
    N3 = (H3 - L3) / len
    dimen1 = (np.log(N1 + N2) - np.log(N3)) / np.log(2)
    dimen = np.where((N1 > 0) & (N2 > 0) & (N3 > 0), dimen1, np.roll(dimen1, 1))
    alpha1 = np.exp(w * (dimen - 1))
    oldalpha = np.where(alpha1 > 1, 1, np.where(alpha1 < 0.01, 0.01, alpha1))
    oldN = (2 - oldalpha) / oldalpha
    N = (((SC - FC) * (oldN - 1)) / (SC - 1)) + FC
    alpha_ = 2 / (N + 1)
    alpha = np.where(alpha_ < 2 / (SC + 1), 2 / (SC + 1), np.where(alpha_ > 1, 1, alpha_))
    out = np.zeros_like(df[src])
    for i in range(1, len(df)):
        out[i] = (1 - alpha[i]) * out[i - 1] + alpha[i] * df[src].iloc[i]
    return pd.Series(out, index=df.index, name='FRAMA')
