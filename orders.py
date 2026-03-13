import config
from config import client
import oandapyV20.endpoints.orders as orders


def place_order(stop_loss=None, take_profit=None, type="MARKET", instrument="EUR_USD", units="1"):
    try:
        data = {
            "order": {
                "instrument": instrument,
                "units": units,
                "type": type.upper(),
                "stopLossOnFill": {"price": f"{stop_loss:.3f}"},
                "takeProfitOnFill": {"price": f"{take_profit:.3f}"},

            }
        }
    except:
        data = {
            "order": {
                "instrument": instrument,
                "units": units,
                "type": type.upper(),
            }
        }

    r = orders.OrderCreate(config.OANDA_ACCOUNT_ID, data=data)
    client.request(r)
    try:
        print(f"Placed order for {instrument} with stop loss at {round(stop_loss, 3)} and take profit at {round(take_profit, 3)}")
    except:
        print(f"Placed order for {instrument}")