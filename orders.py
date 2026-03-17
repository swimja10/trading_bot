import requests
from config import OANDA_PRACTICE_API, OANDA_ACCOUNT_ID, headers

def place_oanda_order(order_type, instrument, units, stop_loss, take_profit):
    url = OANDA_PRACTICE_API + f"/v3/accounts/{OANDA_ACCOUNT_ID}/orders"
    data = {
            "order": {
                "instrument": instrument.upper(),
                "units": str(units),
                "type": order_type.upper(),
                "stopLossOnFill": {"price": f"{stop_loss:.5f}"},
                "takeProfitOnFill": {"price": f"{take_profit:.5f}"},
                "timeInForce": "FOK",
                "positionFill": "DEFAULT",
            }
        }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return f"Placed order for {instrument} with stop loss at {round(stop_loss, 3)} and take profit at {round(take_profit, 3)}"
