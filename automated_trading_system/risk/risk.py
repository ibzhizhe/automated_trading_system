class RiskManager:
    def __init__(self, client):
        self.client = client

    def evaluate_risk(self):
        self._print_balance()

    def _print_balance(self):
        balance = self.client.fetch_balance()
        if balance:
            print(f"当前账户余额: {balance['data'][0]['bal']}")
        else:
            print("无法获取账户余额")