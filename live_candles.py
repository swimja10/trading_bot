import oandapyV20.endpoints.instruments as instruments
import pandas as pd
from config import client

def live_candles(granularity="M15", instrument="EUR_USD"):
    params = {
        "granularity" : granularity,
        "price": "A" # Ask price
    }

    r = instruments.InstrumentsCandles(instrument, params=params)
    candles = client.request(r)['candles']

    data = []

    for c in candles:
        if c["complete"]:
            data.append({
                "time": c["time"],
                "open": float(c["ask"]["o"]),
                "high": float(c["ask"]["h"]),
                "low": float(c["ask"]["l"]),
                "close": float(c["ask"]["c"])
            })

    candles = pd.DataFrame(data)
    candles["time"] = pd.to_datetime(candles["time"])
    return candles
