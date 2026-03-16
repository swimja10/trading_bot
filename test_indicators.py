from indicators.moving_averages import SMA
from candles import get_live_candles, get_live_ticks, get_backtest_candles
import time
from datetime import datetime, timezone

# def run_bot():
#     print("starting trading bot")
#     last_checked = None
    
#     while True:
#         current_time = datetime.now(timezone.utc)
#         if current_time.minute % 1 == 0 and current_time.second < 10:
#             if last_checked != current_time.minute:
#                 print(f"Current time: {current_time}")
#                 sma = SMA(get_live_candles(granularity="M1", instrument="EUR_USD")["close"], 5)
#                 print(sma)
#                 last_checked = current_time.minute 

#             time.sleep(1)
#         else:
#             pass

# run_bot()

print(get_backtest_candles(instrument="EUR_USD", granularity="H1", from_time="01/01/2026", to_time="01/03/2026"))