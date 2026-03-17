import requests
from config import OANDA_ACCOUNT_ID, OANDA_PRACTICE_API, headers

def get_oanda_open_trade_count():
    url = OANDA_PRACTICE_API + f"/v3/accounts/{OANDA_ACCOUNT_ID}/trades"
    query = {
        "state": "OPEN"
    }
    response = requests.get(url, headers=headers, params=query)
    json_response = response.json()
    return len(json_response['trades'])

def get_oanda_account_balance():
    url = OANDA_PRACTICE_API + f"/v3/accounts/{OANDA_ACCOUNT_ID}/summary"
    response = requests.get(url, headers=headers)
    json_response = response.json()
    return json_response['account']["balance"]

print(get_oanda_open_trade_count())