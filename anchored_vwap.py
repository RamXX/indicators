from common import *

def anchored_vwap(dff, anchor_type, specific_date=None):
    """ 
    Returns the anchored VWAP for either a specific date or an anchor type. 
    Allowed values are 'specific_date', '52-week_high', 'month_to_date', 'quarter_to_date', 'year_to_date'". 
    The input dataframe needs to be in OHLCV format with lowercase fields.
    """
    df = dff.copy()
    if not isinstance(df, pd.DataFrame) or not all(col in df.columns for col in ['open', 'high', 'low', 'close', 'volume']):
        raise ValueError('The input should be a Pandas DataFrame with columns: open, high, low, close, and volume')

    if anchor_type not in ['specific_date', '52-week_high', 'month_to_date', 'quarter_to_date', 'year_to_date']:
        raise ValueError("Invalid anchor type. Allowed values are 'specific_date', '52-week_high', 'month_to_date', 'quarter_to_date', 'year_to_date'")

    if anchor_type == 'specific_date' and specific_date is None:
        raise ValueError("For anchor_type 'specific_date', you must provide a specific date as a datetime object")

    if anchor_type == 'specific_date':
        anchor_date = specific_date
    elif anchor_type == '52-week_high':
        high_52_week = df['high'].rolling(window=252).max()
        anchor_date = high_52_week.idxmax()
    elif anchor_type == 'month_to_date':
        anchor_date = df.index.to_period('M').to_timestamp()
    elif anchor_type == 'quarter_to_date':
        anchor_date = df.index.to_period('Q').to_timestamp()
    elif anchor_type == 'year_to_date':
        anchor_date = df.index.to_period('Y').to_timestamp()

    # Calculate the typical price and volume-weighted typical price
    df['typical_price'] = (df['high'] + df['low'] + df['close']) / 3
    df['vwap_numerator'] = df['typical_price'] * df['volume']
    
    # Filter the DataFrame based on the anchor date
    df_filtered = df[df.index >= anchor_date]

    # Calculate the anchored VWAP
    vwap = df_filtered['vwap_numerator'].cumsum() / df_filtered['volume'].cumsum()

    return vwap
