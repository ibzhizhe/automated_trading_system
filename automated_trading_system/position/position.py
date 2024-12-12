

class PositionManager:
    def __init__(self, client):
        self.client = client

    def get_positions(self):
        # 从OKX获取当前持仓信息
        positions = self.client.account_api.get_positions()
        return positions['data'] if 'data' in positions else []

    def print_positions(self):
        # 格式化并打印仓位信息
        positions = self.get_positions()
        if positions:
            for pos in positions:
                print(f"交易对: {pos['instId']}")
                print(f"持仓数量: {pos['pos']}")
                print(f"平均入场价: {pos['avgPx']}")
                print(f"未实现盈亏: {pos['upl']}")
                print(f"已实现盈亏: {pos['realisedPnl']}")
                print("---")
        else:
            print("当前无持仓信息")
