from strategy.strategy import StrategyManager
from position.position import PositionManager
from monitor.monitor import SystemMonitor
from engine.engine import TradingEngine
from charts.charts import KLineChart
from client.client import OKXClient
from risk.risk import RiskManager
from config import CONFIG


# 主程序入口
def main():
    # 初始化 OKX 客户端，传入配置中的 API 密钥、API 密钥密码和密码短语
    okx_client = OKXClient(CONFIG['api_key'], CONFIG['api_secret'], CONFIG['passphrase'])
    # 创建系统监控器实例
    system_monitor = SystemMonitor()
    # 创建 K 线图实例，使用 OKX 客户端
    kline_chart = KLineChart(okx_client)
    # 创建仓位管理器实例，使用 OKX 客户端
    position_manager = PositionManager(okx_client)
    # 创建策略管理器实例，使用 OKX 客户端
    strategy_manager = StrategyManager(okx_client)
    # 创建风险管理器实例，使用 OKX 客户端
    risk_manager = RiskManager(okx_client)

    # 使用上面初始化的组件创建交易引擎
    engine = TradingEngine(strategy_manager, risk_manager, system_monitor, position_manager, kline_chart)
    # 启动交易引擎
    engine.run()


if __name__ == "__main__":
    main()
