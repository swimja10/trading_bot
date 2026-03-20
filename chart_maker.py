import mplfinance as mpf
from candles import * 
import threading
import queue
import matplotlib.pyplot as plt
from candles import get_live_ticks, get_live_candles
import requests
import pandas

def chart_maker(candles):
    OHLC_data = candles[["open", "high", "low", "close"]]
    OHLC_data = OHLC_data[-500:]
    return OHLC_data

# mpf.plot(chart_maker(get_backtest_candles(granularity='S30', instrument='EUR_USD', from_time='11/03/2020', to_time='11/04/2020')), type = 'candle' ,style='charles')

def plotting_live_tick_data():
    class sliding_window:
        def __init__(self, length):
            self.data = ([0]*length)
        def add(self, element):
            self.data.append(element)
            self.data.pop(0)

    def OANDA_connect(instrument, ticks_queue):
        while True:
            tick = get_live_ticks(instrument)
            ticks_queue.put(tick)


    instrument = "EUR_USD"

    pipe = queue.Queue()
    data_receiver_thread = threading.Thread(target = OANDA_connect, args = (instrument, pipe))
    data_receiver_thread.start()

    def get_ticks(ticks_queue):
        while True:
            tick = ticks_queue.get()

            bid = float(tick["bid"].iloc[-1])
            ask = float(tick["ask"].iloc[-1])
            bids.add(bid)
            asks.add(ask)
            # print(bid, ask)

    window_size = 60
    bids = sliding_window(window_size)
    asks = sliding_window(window_size)
    trading_algo_thread = threading.Thread(target = get_ticks, args = (pipe,))
    trading_algo_thread.start()

    while bids.data[0] == 0:
        pass

    fig = plt.figure()
    ax = fig.add_subplot()

    line1, = ax.plot(bids.data)
    line2, = ax.plot(asks.data)

    while True:
        line1.set_ydata(bids.data)
        line2.set_ydata(asks.data)
        plt.ylim(min(bids.data) - 0.0001, max(asks.data) + 0.0001)
        fig.canvas.draw()
        plt.pause(1)

mpf.plot(chart_maker(get_live_candles(granularity="H4", instrument="EUR_USD")), type = 'candle' ,style='charles')