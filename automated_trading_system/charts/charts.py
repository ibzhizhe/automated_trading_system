# charts/charts.py

import mplfinance as mpf
import pandas as pd
import matplotlib.pyplot as plt
from utils.global_vars import MAX_TRADES_PER_DAY


class KLineChart:
    def __init__(self, client):
        self.client = client
        self.last_plot_time = 0
        self.plot_interval = 600  # 图表更新间隔，单位为秒，示例值为10分钟

    def fetch_price_data(self, symbol, timeframe='1m', limit=100):
        # 从OKX获取K线数据
        candles = self.client.market_api.get_candlesticks(instId=symbol, bar=timeframe, limit=limit)
        if 'data' not in candles:
            print("无法获取K线数据")
            return None

        # 格式化数据到DataFrame
        df = pd.DataFrame(candles['data'],
                          columns=['time', 'open', 'high', 'low', 'close', 'volume', 'currency_volume'])
        df['time'] = pd.to_datetime(df['time'], unit='ms')
        df.set_index('time', inplace=True)
        df = df[['open', 'high', 'low', 'close', 'volume']].astype(float)
        return df

    def plot_kline(self, symbol, force_plot=False):
        import time
        current_time = time.time()

        # 控制图表更新频率，避免过度绘图
        if not force_plot and (current_time - self.last_plot_time < self.plot_interval):
            return

        df = self.fetch_price_data(symbol)
        if df is not None:
            # 创建一个新的图形
            fig, ax = plt.subplots(figsize=(15, 10))

            # 设置图表样式
            mpf.plot(df, type='candle', style='charles', title=f'{symbol} K线图',
                     volume=True, figratio=(15, 10), ax=ax, show_nontrading=False)

            # 添加当前交易次数限制的文本信息
            ax.text(0.02, 0.98, f'今日交易限制: {MAX_TRADES_PER_DAY}', transform=ax.transAxes,
                    verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.5))

            plt.show()
            self.last_plot_time = current_time
        else:
            print("无法绘制K线图")

    def close_plot(self):
        plt.close('all')
