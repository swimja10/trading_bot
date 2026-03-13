from live_candles import live_candles
from orders import place_order
from datetime import datetime, timezone
import time



def test_trade():
    print("Trade initiated")
    place_order()


def test_bot():
    test_trade()


test_bot()