import matplotlib.pyplot as plt
from indicators.moving_averages import SMA
from candles import get_backtest_candles

def simulate_trade(current_position, new_position, current_price, entry_price, equity):
    if current_position != 0 and current_position != new_position:
        pnl = (current_price - entry_price) * current_position
        equity += pnl
        action = "Sell" if current_position > 0 else "Buy"
        print(f"{action} to close position at {current_price} | Realized PnL: ${pnl:.2f} | Equity: ${equity:.2f}")

    if current_position != new_position and new_position != 0:
        action = "Buy" if new_position > 0 else "Sell"
        print(f"{action} to open position at {current_price}")
        entry_price = current_price

    return new_position, entry_price, equity

initial_capital = 1000
equity = initial_capital
market_position = 0
entry_price = 0
equity_timeseries = []
position_size = equity * 50
closed_prices = get_backtest_candles(granularity='H4', instrument='EUR_USD', from_time='11/03/2005', to_time='12/06/2005')
candles_done = []
print(closed_prices)

for candle in closed_prices:
    candles_done.append(candle)
    equity_timeseries.append(equity)
    previous_candle = candles_done[:-1]

    try:
        new_position = market_position
        # Longing
        if SMA(candles_done, 5) > SMA(candles_done, 8) and SMA(previous_candle, 5) < SMA(previous_candle, 8):
            new_position = position_size
        # Shorting
        elif SMA(candles_done, 5) < SMA(candles_done, 8) and SMA(previous_candle, 5) > SMA(previous_candle, 8):
            new_position = -position_size
            
        market_position, entry_price, equity = simulate_trade(
            market_position, new_position, candles_done[:-1], entry_price, equity
        )
    except:
        pass

plt.plot(equity_timeseries)
plt.title("Simple Linear Backtest")
plt.show()