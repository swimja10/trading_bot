import pandas_ta as ta
from orders import place_order
from oanda_account_details import get_oanda_account_balance, get_oanda_open_trade_count
from oandapyV20.exceptions import V20Error
from datetime import datetime
from candles import get_live_candles
from datetime import datetime, timezone
import time
import sys


units = (get_oanda_account_balance() * 50.0) * .25
units_str = str(int(units))

def calculate_indicators(candles):
    #EMAS
    candles["EMA_5"] = ta.ema(candles["close"], length = 5)
    candles["EMA_8"] = ta.ema(candles["close"], length = 8)
    candles["SMA_5"] = ta.sma(candles["close"], length = 8)

    return candles

# Function to check for EMA Crossover signals

def ema_crossover(candles, instrument):
    #Check if the 5-period EMA crosses above the 8-period EMA
    last_candle = candles.iloc[-1]
    previous_candle = candles.iloc[-2]

    # Crossover Buy Signal (EMA 5 crosses above EMA 8)
    if last_candle['EMA_5'] > last_candle['EMA_8'] and previous_candle['EMA_5'] < previous_candle['EMA_8']:
        print("Buy signal: EMA 5 crossed above EMA 8")
        entry_price = last_candle['close']
        PIP_VALUE = 0.0001          #EURUSD
        PIPS_DESIRED = 15
        DISTANCE = PIPS_DESIRED * PIP_VALUE
        stop_loss = entry_price - DISTANCE
        take_profit = entry_price + .0005
        place_order(stop_loss=stop_loss, take_profit=take_profit, type="MARKET", instrument=instrument, units=units_str)
    else:
        print("Strat not met")


def run_bot():
    print("starting trading bot")
    last_checked = None
    
    while True:
        current_time = datetime.now(timezone.utc)
        try:
            if get_oanda_open_trade_count() == 0:
                if current_time.minute % 15 == 0 and current_time.second < 10:
                    if last_checked != current_time.minute:
                        print(f"Current time: {current_time}")
                        print("Checking for trade signals")
                        ema_crossover(calculate_indicators(get_live_candles(granularity="M15", instrument="EUR_USD")), "EUR_USD")
                        last_checked = current_time.minute

                time.sleep(1)
            else:
                pass
        except KeyboardInterrupt:
            print("\nBYE!")
            sys.exit()
        except Exception as e:
            print(f"Error occurred at {current_time}: {e}")
            pass
        except V20Error:
            print(f"V20 error occured at {current_time}")
            pass

run_bot()