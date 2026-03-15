import oandapyV20.endpoints.instruments as instruments
import pandas as pd
from config import client
import json


def live_candles(granularity, instrument):
    params = {
        "granularity": granularity,
        "price": "A"
    }

    r = instruments.InstrumentsCandles(instrument, params=params)
    raw_candles = client.request(r)["candles"]
    normalized_candles = normalize_oanda_candles(raw_candles)
    return candles_to_dataframe(normalized_candles)


def normalize_oanda_candles(raw_candles):
    normalized = []

    for candle in raw_candles:
        if candle["complete"]:
            normalized.append({
                "time": candle["time"],
                "open": float(candle["ask"]["o"]),
                "high": float(candle["ask"]["h"]),
                "low": float(candle["ask"]["l"]),
                "close": float(candle["ask"]["c"]),
            })

    return normalized

def normalize_backtest_candles(file_name):
    normalized = []

    with open(file_name, "r") as f:
        data = json.load(f)
    
    for candle in data['candles']:
        normalized.append(build_candle(
            time=candle["time"],
            open=candle["mid"]["o"],
            high=candle["mid"]["h"],
            low=candle["mid"]["l"],
            close=candle["mid"]["c"],
        ))
    return candles_to_dataframe(normalized)

def build_candle(time, open, high, low, close):
    return {
        "time": time,
        "open": float(open),
        "high": float(high),
        "low": float(low),
        "close": float(close),
    }

def candles_to_dataframe(candles):
    df = pd.DataFrame(candles)
    df["time"] = pd.to_datetime(df["time"])
    return df