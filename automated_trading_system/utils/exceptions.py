class TradingError(Exception):
    """交易过程中发生的通用错误。"""
    pass


class APIError(TradingError):
    """与API调用相关的错误。"""
    pass


class StrategyError(TradingError):
    """与策略执行相关的错误。"""
    pass


class RiskError(TradingError):
    """与风险评估相关的错误。"""
    pass
