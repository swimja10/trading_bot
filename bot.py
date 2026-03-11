import pandas_ta as ta
import config
from config import client
import random
import oandapyV20.endpoints.orders as orders
from oanda_account_details import get_account_balance, get_trade_count
from oandapyV20.exceptions import V20Error
from datetime import datetime
import time
from live_candles import live_EURUSD_candles
from datetime import datetime, timezone
import time

# instrument = "EUR_USD"

units = (get_account_balance() * 50.0) * .25
units_str = str(int(units))
# test_units = 1

def calculate_indicators(candles):
    #EMAS
    candles["EMA_5"] = ta.ema(candles["close"], length = 5)
    candles["EMA_8"] = ta.ema(candles["close"], length = 8)
    candles["SMA_5"] = ta.sma(candles["close"], length = 8)

    # ATR
    candles["ATR_14"] = ta.atr(candles["high"], candles["low"], candles["close"], length=14)

    return candles

def place_order(stop_loss, take_profit, instrument, units):
    data = {
        "order": {
            "instrument": instrument,
            "units": units,
            "type": "MARKET",
            "stopLossOnFill": {"price": f"{stop_loss:.3f}"},
            "takeProfitOnFill": {"price": f"{take_profit:.3f}"},

        }
    }

    r = orders.OrderCreate(config.OANDA_ACCOUNT_ID, data=data)
    client.request(r)
    print(f"Placed order for {instrument} with stop loss at {round(stop_loss, 3)} and take profit at {round(take_profit)}")

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
        place_order(stop_loss, take_profit, instrument, units_str)
    else:
        print("Strat not met")

def test_trade(candles, instrument, units):
    print("Trade initiated")
    last_candle = candles.iloc[-1]
    entry_price = last_candle['close']
    PIP_VALUE = 0.0001          #EURUSD
    PIPS_DESIRED = 30
    DISTANCE = PIPS_DESIRED * PIP_VALUE
    stop_loss = entry_price - DISTANCE
    take_profit = entry_price + .0005
    place_order(stop_loss, take_profit, instrument, units)

def candles():
    candles = live_EURUSD_candles("M15")
    candles = calculate_indicators(candles)
    return candles



def run_bot():
    print("starting trading bot")
    last_checked = None
    
    while True:
        current_time = datetime.now(timezone.utc)
        try:
            if get_trade_count() == 0:
                if current_time.minute % 15 == 0 and current_time.second < 10:
                    if last_checked != current_time.minute:
                        print(f"Current time: {current_time}")
                        print("Checking for trade signals")
                        ema_crossover(candles(), "EUR_USD")
                        last_checked = current_time.minute

                time.sleep(1)
            else:
                pass
        except Exception as e:
            print(f"Error occurred at {current_time}: {e}")
            pass

def test_bot():
    test_trade(candles(), "EUR_USD", 1)

def test_bot_1M():
    last_checked = None

    while True:
        current_time = datetime.now(timezone.utc)
        candle_data = calculate_indicators(candles())
        last_candle = candle_data.iloc[-1]
        if current_time.minute % 1 == 0 and current_time.second < 10:
            if last_checked != current_time.minute:
                print(f"Current time: {current_time}")
                print(last_candle['SMA_5'])
                last_checked = current_time.minute

        time.sleep(1)

run_bot()
# test_bot()
# test_bot_1M()