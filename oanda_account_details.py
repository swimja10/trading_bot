import config
from config import OANDA_ACCOUNT_ID, client
import oandapyV20.endpoints.accounts as accounts
import oandapyV20.endpoints.trades as trades

def get_trade_count():
    r = accounts.AccountDetails(OANDA_ACCOUNT_ID)
    openTrade = client.request(r)['account']['openPositionCount']
    return openTrade

def get_account_balance():
    r = accounts.AccountDetails(OANDA_ACCOUNT_ID)
    raw_balance = client.request(r)['account']["balance"]
    return float(raw_balance)