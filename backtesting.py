import json
import matplotlib.pyplot as plt
from indicators.moving_averages import SMA

with open("EURUSD1M.json", "r") as f:
    data = json.load(f)

initial_capital = 1000
equity = initial_capital
market_position = 0
last_price = 0
equity_timeseries = []
position_size = 10000
closed_prices = []

for candle in data['candles']:

    o = float(candle['mid']['o'])
    h = float(candle['mid']['h'])
    l = float(candle['mid']['l'])
    c = float(candle['mid']['c'])


    equity_timeseries.append(equity)
    last_price = c
    closed_prices.append(last_price)
    previous_candle = closed_prices[:-1]

    print(candle['time'])
    if last_price != 0:
        equity += (c - last_price) * market_position

    if SMA(closed_prices, 5) > SMA(closed_prices, 8) and SMA(previous_candle, 5) < SMA(previous_candle, 8):
        market_position = position_size
        print("Bought")
    elif SMA(closed_prices, 5) < SMA(closed_prices, 8) and SMA(previous_candle, 5) > SMA(previous_candle, 8):
        market_position = -position_size
        print("Shorted")

plt.plot(equity_timeseries)
plt.title("Simple Linear Backtest")
plt.show()

