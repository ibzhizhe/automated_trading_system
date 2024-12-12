import logging

from okx import Trade, Account, MarketData


class OKXClient:
    def __init__(self, api_key, api_secret, passphrase):
        self.trade_api = Trade.TradeAPI(api_key, api_secret, passphrase, False, '0')
        self.account_api = Account.AccountAPI(api_key, api_secret, passphrase, False, '0')
        self.market_api = MarketData.MarketAPI('0')

    def fetch_balance(self):

        account_info = self.account_api.get_account()
        if account_info and 'data' in account_info and account_info['data']:
            # 'bal' 可能不在直接返回的数据中，查找可能的其他键
            for account in account_info['data']:
                for key, value in account.items():
                    if key.lower() == 'bal' or key.lower() == 'balance':
                        return value
            return "无法找到余额信息"
        return "无法获取账户信息"

    def create_order(self, instId, tdMode, side, ordType, sz, px=None):
        order_params = {
            'instId': instId,
            'tdMode': tdMode,
            'side': side,
            'ordType': ordType,
            'sz': sz,
        }
        if px:
            order_params['px'] = px
        return self.trade_api.place_order(**order_params)

    def fetch_ticker(self, instId):
        ticker = self.market_api.get_ticker(instId=instId)
        return ticker['data'][0] if ticker['data'] else None
