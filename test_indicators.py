from indicators.moving_averages import SMA
from live_candles import live_candles
import time
from datetime import datetime, timezone

def run_bot():
    print("starting trading bot")
    last_checked = None
    
    while True:
        current_time = datetime.now(timezone.utc)
        if current_time.minute % 1 == 0 and current_time.second < 10:
            if last_checked != current_time.minute:
                print(f"Current time: {current_time}")
                sma = SMA(live_candles("M1")["close"], 5)
                print(sma)
                last_checked = current_time.minute 

            time.sleep(1)
        else:
            pass

run_bot()
