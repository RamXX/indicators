from common import *

def SuperMA(df: pd.DataFrame, MAtype='SMA', timeperiod=21, **kwargs):
    """ 
    Calculates multiple moving averages with a single function. It corrects some mistakes found in other multi-MA functions.
    This one picks some from TA-Lib (when possible) and others from Pandas-ta as needed.
    """
    dataframe = df.copy()
    hl2 = (dataframe['high'] + dataframe['low']) / 2
    opt = {
        'EMA': ta.EMA(dataframe, timeperiod=timeperiod),
        'SMA': ta.SMA(dataframe, timeperiod=timeperiod),
        'DEMA': ta.DEMA(dataframe, timeperiod=timeperiod),
        'TRIMA': ta.TRIMA(dataframe, timeperiod=timeperiod),
        'MAMA': ta.MAMA(dataframe, timeperiod=timeperiod), # MAMA returns two series, one for MAMA and one for FAMA. Common params are 0.25, 0.025.
        'KAMA': ta.KAMA(dataframe, timeperiod=timeperiod),
        'ALMA': ta.ALMA(dataframe, timeperiod=timeperiod),
        'T3': ta.T3(dataframe, timeperiod=timeperiod),
        'VIDYA': pta.vidya(dataframe['close'], length=timeperiod),
        'TEMA': ta.TEMA(dataframe, timeperiod=timeperiod),
        'WMA': ta.WMA(dataframe, timeperiod=timeperiod),
        'VWMA': pta.vwma(dataframe['close'], dataframe['volume'], length=timeperiod),
        'ZLEMA': pta.zlma(dataframe['close'], length=timeperiod, mamode='linreg'),
        'HMA': pta.hma(dataframe['close'], length=timeperiod),
        'VWAP': pta.vwap(dataframe['high'], dataframe['low'], dataframe['close'], dataframe['volume'])
    }
    return pd.Series(opt.get(MAtype, 'Invalid Indicator'))