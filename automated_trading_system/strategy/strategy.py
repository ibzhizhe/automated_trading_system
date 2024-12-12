from strategies.btc_usdt_strategy import BTCUSDTStrategy
from strategies.ema_cross import EMACrossStrategy


class StrategyManager:
    """
    策略管理器类，负责管理和执行一组交易策略。
    """

    def __init__(self, client):
        """
        初始化策略管理器，传入客户端对象，并初始化策略列表。
        """
        self.client = client
        self.strategies = [BTCUSDTStrategy(client)]

    def execute_strategies(self):
        """
        执行所有策略的 execute 方法。
        """
        for strategy in self.strategies:
            strategy.execute()
