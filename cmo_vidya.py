from common import *


def vidya_modified(df, length=9, fixed_cmo_length=True, use_cmo=True):
    """ 
    VIDYA Moving Average. It includes the CMO modifications (default)). The input dataframe needs to be in OHLCV format with lowercase fields.
    """
    src = df['close']
    alpha = 2 / (length + 1)

    # Calculate momentum
    momm = src.diff()

    # Calculate positive and negative momentum
    m1 = momm.where(momm >= 0, 0)
    m2 = (-momm).where(momm < 0, 0)

    # Calculate the sum of positive and negative momentum
    cmo_length = 9 if fixed_cmo_length else length
    sm1 = m1.rolling(window=cmo_length).sum()
    sm2 = m2.rolling(window=cmo_length).sum()

    # Calculate Chande Momentum Oscillator (CMO)
    chande_mo = 100 * (sm1 - sm2) / (sm1 + sm2)

    # Calculate scaling factor (k) using CMO or standard deviation
    if use_cmo:
        k = chande_mo.abs() / 100
    else:
        k = src.rolling(window=length).std()

    # Calculate VIDYA
    vidya = pd.Series(np.nan, index=df.index)
    for i in range(len(df)):
        if i == 0 or np.isnan(k[i]) or np.isnan(src[i]):
            vidya.iloc[i] = np.nan
        else:
            vidya.iloc[i] = alpha * k[i] * src[i] + (1 - alpha * k[i]) * vidya.iloc[i-1]

    return vidya

