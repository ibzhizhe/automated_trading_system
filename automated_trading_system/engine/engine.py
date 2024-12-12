import time


class TradingEngine:
    def __init__(self, strategy_manager, risk_manager, system_monitor, position_manager, kline_chart):
        self.strategy_manager = strategy_manager
        self.risk_manager = risk_manager
        self.system_monitor = system_monitor
        self.position_manager = position_manager
        self.kline_chart = kline_chart

    def run(self):
        while True:
            try:
                self.strategy_manager.execute_strategies()  # 执行策略
                self.risk_manager.evaluate_risk()
                self.system_monitor.check_health()
                self.position_manager.print_positions()  # 打印仓位信息

                # 每10轮交易展示一次K线图，或手动强制展示
                if time.time() % (10 * 60) < 60:  # 假设每分钟执行一次，每10分钟展示一次
                    self.kline_chart.plot_kline('BTC-USDT')
                else:
                    # 每分钟检查是否需要更新图表，但不展示
                    self.kline_chart.plot_kline('BTC-USDT', force_plot=False)

                time.sleep(60)  # 每分钟执行一次
            except Exception as e:
                self.system_monitor.log_error(e)
                self.kline_chart.close_plot()  # 关闭所有图表
                break
