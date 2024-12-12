import pandas as pd


class BTCUSDTStrategy:
    def __init__(self, client):
        self.client = client
        self.symbol = 'BTC-USDT-SWAP'
        self.leverage = 100
        self.amount = 0.001  # 开仓0.001个BTC
        self.stop_loss_percentage = 0.05  # 5% 止损

    def fetch_price_data(self, limit=100):
        candles = self.client.market_api.get_candlesticks(instId=self.symbol, bar='1m', limit=limit)
        if 'data' not in candles:
            print("无法获取K线数据")
            return None

        df = pd.DataFrame(candles['data'],
                          columns=['time', 'open', 'high', 'low', 'close', 'volume', 'currency_volume', 'confirm',
                                   'bar_index'])
        df['time'] = pd.to_numeric(df['time'])
        df['time'] = pd.to_datetime(df['time'], unit='ms')
        df.set_index('time', inplace=True)
        df = df[['open', 'high', 'low', 'close', 'volume']].astype(float)
        return df

    def calculate_ema(self, data, period):
        # 计算EMA
        ema = data['close'].ewm(span=period, adjust=False).mean()
        return ema

    def execute(self):
        data = self.fetch_price_data()
        if data is None:
            return

        # 计算EMA12和EMA144
        ema12 = self.calculate_ema(data, 12)
        ema144 = self.calculate_ema(data, 144)

        # 获取当前价格
        ticker = self.client.fetch_ticker(self.symbol)
        if not ticker:
            print("无法获取行情数据")
            return

        current_price = float(ticker['last'])

        # 检查EMA交叉情况
        if ema12.iloc[-1] > ema144.iloc[-1] and ema12.iloc[-2] <= ema144.iloc[-2]:  # EMA12上穿EMA144
            self.open_position('buy', current_price)
        elif ema12.iloc[-1] < ema144.iloc[-1] and ema12.iloc[-2] >= ema144.iloc[-2]:  # EMA12下穿EMA144
            self.close_position('buy', current_price)
            self.open_position('sell', current_price)
        elif ema12.iloc[-1] > ema144.iloc[-1] and ema12.iloc[-2] >= ema144.iloc[-2]:  # EMA12在EMA144上方
            self.close_position('sell', current_price)
        # 其他情况保持不变

    def open_position(self, side, price):
        self.client.trade_api.set_leverage(instId=self.symbol, lever=self.leverage, mgnMode='cross')

        order = self.client.create_order(
            instId=self.symbol,
            tdMode='cross',  # 交叉保证金模式
            side=side,  # 'buy' or 'sell'
            ordType='market',  # 市价单
            sz=str(self.amount * self.leverage)  # 注意这里的sz应该是字符串，因为API期望的是字符串型的数量
        )
        stop_loss_price = self.calculate_stop_loss(price, side)
        print(f"开仓: {side}, 当前价格: {price}, 止损价: {stop_loss_price}, 订单详情: {order}")

    def close_position(self, side, price):
        order = self.client.create_order(
            instId=self.symbol,
            tdMode='cross',
            side='sell' if side == 'buy' else 'buy',  # 平多仓用sell，平空仓用buy
            ordType='market',
            sz=str(self.amount * self.leverage)  # 假设我们开仓和平仓的数量相等
        )
        print(f"平仓: {side}, 当前价格: {price}, 订单详情: {order}")

    def calculate_stop_loss(self, price, side):
        if side == 'buy':
            return price * (1 - self.stop_loss_percentage)
        else:
            return price * (1 + self.stop_loss_percentage)