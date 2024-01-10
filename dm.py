from common import *

def demark_pivot_points(df, period):
    """ 
    Returns a dataframe with the DeMark Pivot levels.
    The periods can be daily to yearly. The input dataframe needs to be in OHLCV format with lowercase fields.
    """
    if not isinstance(df, pd.DataFrame) or not all(col in df.columns for col in ['open', 'high', 'low', 'close']):
        raise ValueError('The input should be a Pandas DataFrame with columns: open, high, low, and close')

    if period not in ['daily', 'weekly', 'monthly', 'quarterly', 'yearly']:
        raise ValueError("Invalid period. Allowed values are 'daily', 'weekly', 'monthly', 'quarterly', 'yearly'")

    if period == 'daily':
        df_resampled = df.copy()
    else:
        resample_rule = {
            'weekly': 'W',
            'monthly': 'M',
            'quarterly': 'Q',
            'yearly': 'Y'
        }
        df_resampled = df.resample(resample_rule[period], closed='right', label='right').agg({'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last'})

    def calculate_demark_pivot(row):
        x = 0
        if row['close'] < row['open']:
            x = row['high'] + 2 * row['low'] + row['close']
        elif row['close'] > row['open']:
            x = 2 * row['high'] + row['low'] + row['close']
        else:
            x = row['high'] + row['low'] + 2 * row['close']

        pivot = x / 4
        support = 2 * pivot - row['high']
        resistance = 2 * pivot - row['low']

        return pd.Series({'pivot': pivot, 'support': support, 'resistance': resistance})

    demark_pivot_points_df = df_resampled.apply(calculate_demark_pivot, axis=1)

    return demark_pivot_points_df
