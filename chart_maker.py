import mplfinance as mpf
from candles import * 

def chart_maker(candles):
    OHLC_data = candles[["open", "high", "low", "close"]]
    OHLC_data = OHLC_data[-500:]
    return OHLC_data

mpf.plot(chart_maker(get_backtest_candles(granularity='H4', instrument='EUR_USD', from_time='11/03/2005', to_time='12/06/2005')), type = 'candle' ,style='charles')