import json
import matplotlib.pyplot as plt
from indicators.moving_averages import SMA

# Load your data
with open("EURUSD1M.json", "r") as f:
    data = json.load(f)

# Simulation variables
initial_capital = 1000
equity = initial_capital
market_position = 0
last_price = 0
equity_timeseries = []
position_size = 10000

# Simple linear loop - no threading required
for candle in data['candles']:
    if not candle['complete']:
        continue
    
    # Extract prices
    o = float(candle['mid']['o'])
    h = float(candle['mid']['h'])
    l = float(candle['mid']['l'])
    c = float(candle['mid']['c'])
    
    # Update equity based on price movement of current position
    if last_price != 0:
        equity += (c - last_price) * market_position
    
    equity_timeseries.append(equity)
    last_price = c
    print(last_price)

#     # Strategy Logic (Trend following example)
#     # Buy if price closes higher than open, Sell if it closes lower
#     if SMA(last_price, 5) > SMA(last_price, 8):
#         market_position = position_size 
#     #     # Close short if exists and go long
#     #     market_position = position_size
#     # elif c < o and market_position >= 0:
#     #     # Close long if exists and go short
#     #     market_position = -position_size

# # Final Plot
# plt.plot(equity_timeseries)
# plt.title('Simple Linear Backtest')
# plt.show()