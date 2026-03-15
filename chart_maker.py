import mplfinance as mpf
from candles import * 

def chart_maker(candles):
    OHLC_data = candles[["open", "high", "low", "close"]]
    OHLC_data = OHLC_data[-500:]
    return OHLC_data

mpf.plot(chart_maker(normalize_backtest_candles("EURUSD1M_test.json")), type = 'candle' ,style='charles')