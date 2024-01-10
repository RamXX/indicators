from common import *

def add_tp_sl(df, buy_signals, sell_signals, use_atr_sl=True, use_atr_tp=True, sl_mult=1.5, tp_mult=3.5, trailing_sl=False, trailing_sl_mult=1.0):
    """ 
    Modifies the sell signals to include ATR-based stop-loss or take-profit levels, either static or using trailing stop loss. 
    Those will be triggered *in addition to* the sell_signals already present.
    The input dataframe needs to be in OHLCV format with lowercase fields. The buy/sell signals are boolean series.
    It returns a modified series of booleans. It will NOT modify the original input.
    If trailing stop loss is used, it takes precedence over other methods. TODO: a trigger mechanism after a static tp level is reached.
    """
    if not (use_atr_sl & use_atr_tp & trailing_sl):
        return sell_signals
    
    prices = df['close']
    atr = ta.ATR(df['high'], df['low'], prices, timeperiod=14)
    atr_at_purchase = pd.Series(np.where(buy_signals, atr, np.nan))
    atr_at_purchase.ffill(inplace=True)
    sl = prices - (sl_mult * atr)
    tp = prices + (tp_mult * atr)

    if trailing_sl:
        initial_trailing_sl = prices - (trailing_sl_mult * atr)
        # Adjust the trailing SL only on days following buy signals
        adjusted_trailing_sl = initial_trailing_sl.where(buy_signals, np.nan)
        # Use cummax to ensure the SL only increases
        trailing_sl_level = adjusted_trailing_sl.fillna(method='ffill').cummax()
        return (sell_signals) | (prices < sl.shift(1)) | (prices > tp.shift(1)) | (prices < trailing_sl_level.shift(1))
    else:
        if (use_atr_sl & use_atr_tp):
            # We are using a fixed stop loss and take profit values.
            return (sell_signals) | (prices < sl.shift(1)) | (prices > tp.shift(1))
        elif (use_atr_sl & use_atr_tp == False):
            # We are ONLY using a fixed stop loss and we don't care about take profit levels.
            return (sell_signals) | (prices < sl.shift(1))
        elif (use_atr_sl == False & use_atr_tp):
            # We are ONLY using the take-profit level and don't use a stop-loss (not very common).
            return (sell_signals) | (prices > tp.shift(1))