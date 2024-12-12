class EMACrossStrategy:
    """
    EMACrossStrategy 类，实现了基于指数移动平均线（EMA）交叉的交易策略。
    """
    def __init__(self, client):
        self.client = client

    def execute(self):
        """
        执行交易策略，获取指定交易对的最新行情数据并打印。
        """
        # 获取 BTC-USDT 交易对的最新行情数据
        ticker = self.client.fetch_ticker('BTC-USDT')
        if ticker:
            print(f"当前价格: {ticker['last']}")
        else:
            print("无法获取行情数据")