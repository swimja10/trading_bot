import oandapyV20.endpoints.instruments as instruments
import pandas as pd, pandas
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
        clean_time = date_splitter(candle["time"])
        if candle["complete"]:
            normalized.append({
                "date": clean_time["date"],
                "time": clean_time["time"],
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
        clean_time = date_splitter(candle["time"])
        normalized.append(build_candle(
            date=clean_time["date"],
            time=clean_time["time"],
            open=candle["mid"]["o"],
            high=candle["mid"]["h"],
            low=candle["mid"]["l"],
            close=candle["mid"]["c"],
        ))
    return candles_to_dataframe(normalized)

def build_candle(date, time, open, high, low, close):
    return {
        "date": date,
        "time": time,
        "open": float(open),
        "high": float(high),
        "low": float(low),
        "close": float(close),
    }

def candles_to_dataframe(candles):
    df = pd.DataFrame(candles)
    df["timestamp"] = pandas.to_datetime(df['date']) + pandas.to_timedelta(df['time'])
    df.set_index(df['timestamp'], inplace=True)
    return df

def date_splitter(time):
    cleaned_date = {}
    
    time = time.split("T")
    date = time[0]
    cleaned_date["date"] = date

    minute = time[1]
    minute = minute[:8]
    cleaned_date["time"] = minute
    return cleaned_date