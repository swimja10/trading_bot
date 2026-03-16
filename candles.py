import requests
import pandas as pd, pandas
from config import OANDA_ACCOUNT_ID, OANDA_PRACTICE_API, headers
import json
import time

def get_live_candles(granularity, instrument):
    url = OANDA_PRACTICE_API + f"/v3/accounts/{OANDA_ACCOUNT_ID}/candles/latest"
    query = {
            "instrument": instrument,
             "granularity": granularity,
             "PricingComponent": "A",
             }
    response = requests.get(url, headers=headers, params=query)
    json_response = response.json()
    raw_candles = json_response["candles"]
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
                "open": float(candle["mid"]["o"]),
                "high": float(candle["mid"]["h"]),
                "low": float(candle["mid"]["l"]),
                "close": float(candle["mid"]["c"]),
            })

    return normalized


# The time has to be like "01/01/2026"
def get_backtest_candles(granularity, instrument, from_time, to_time):
    url = OANDA_PRACTICE_API + f"/v3/accounts/{OANDA_ACCOUNT_ID}/candles/latest"
    query = {
            "instrument": instrument,
             "granularity": granularity,
             "PricingComponent": "A",
             "from": time.mktime(pd.to_datetime(from_time).timetuple()),
             "to": time.mktime(pd.to_datetime(to_time).timetuple())
             }
    response = requests.get(url, headers=headers, params=query)
    json_response = response.json()
    raw_candles = json_response["candles"]
    normalized_candles = normalize_oanda_candles(raw_candles)
    return candles_to_dataframe(normalized_candles)

def build_candle(date, time, open, high, low, close):
    return {
        "date": date,
        "time": time,
        "open": float(open),
        "high": float(high),
        "low": float(low),
        "close": float(close),
    }

def get_live_ticks(instrument):
    PRICING_PATH =  f"/v3/accounts/{OANDA_ACCOUNT_ID}/pricing"
    url =OANDA_PRACTICE_API + PRICING_PATH
    query = {"instruments": instrument} 
    response = requests.get(url, headers=headers, params=query)
    response_json = response.json()
    raw_ticks = response_json["prices"]
    normalized_ticks = normalize_oanda_ticks(raw_ticks)
    return candles_to_dataframe(normalized_ticks)

def build_ticks(date, time, bid, ask, mid, spread, bid_liquidity, ask_liquidity, tradeable):
    return {
        "date": date,
        "time": time,
        "bid": bid,
        "ask": ask,
        "mid": mid,
        "spread": spread,
        "bid_liquidity": bid_liquidity,
        "ask_liquidity": ask_liquidity,
        "tradeable": tradeable
    }



def normalize_oanda_ticks(raw_ticks):
    normalized = []

    for tick in raw_ticks:
        bid = float(tick["bids"][0]["price"])
        ask = float(tick["asks"][0]["price"])
        clean_time = date_splitter(tick["time"])

        normalized.append(build_ticks(
            date=clean_time["date"],
            time=clean_time["time"],
            bid=bid,
            ask=ask,
            mid=(bid + ask) / 2,
            spread = ask - bid,
            bid_liquidity=tick["bids"][0]["liquidity"],
            ask_liquidity=tick["asks"][0]["liquidity"],
            tradeable=tick["tradeable"]    
        ))
    return normalized

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