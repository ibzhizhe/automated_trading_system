class Order:
    def __init__(self, order_id, symbol, side, quantity, price):
        self.order_id = order_id
        self.symbol = symbol
        self.side = side
        self.quantity = quantity
        self.price = price

    def __repr__(self):
        return f"Order(id={self.order_id}, symbol={self.symbol}, side={self.side}, quantity={self.quantity}, price={self.price})"


class Position:
    def __init__(self, symbol, quantity, entry_price):
        self.symbol = symbol
        self.quantity = quantity
        self.entry_price = entry_price

    def __repr__(self):
        return f"Position(symbol={self.symbol}, quantity={self.quantity}, entry_price={self.entry_price})"
