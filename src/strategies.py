from src.logger import logger

def log_signal(func):
    def decorated(*args, **kwargs):
        signal = func(*args, **kwargs)
        if signal["action"] != "HOLD":
            logger.info(f"Стратегията реши: {signal['action']} {signal['quantity']} бр.")
        return signal
    return decorated

class BaseStrategy:
    def generate_signal(self, current_data: dict, current_cash: float) -> dict:
        raise NotImplementedError()

class SimpleStrategy(BaseStrategy):
    BUY_THRESHOLD = 100.0
    SELL_THRESHOLD = 150.0

    @log_signal
    def generate_signal(self, current_data: dict, current_cash: float) -> dict:
        price = float(current_data["Close"])
        
        if price < self.BUY_THRESHOLD:
            return {"action": "BUY", "quantity": 1}
        elif price > self.SELL_THRESHOLD:
            return {"action": "SELL", "quantity": 1}
        else:
            return {"action": "HOLD", "quantity": 0}
        
class AlwaysBuyStrategy(BaseStrategy):
    @log_signal
    def generate_signal(self, current_data: dict, current_cash: float) -> dict:
        price = float(current_data["Close"])
        if current_cash >= price:
            return {"action": "BUY", "quantity": 1}
        return {"action": "HOLD", "quantity": 0}

class MomentumStrategy(BaseStrategy):
    def __init__(self):
        self.previous_price = None

    @log_signal
    def generate_signal(self, current_data: dict, current_cash: float) -> dict:
        price = float(current_data["Close"])
        
        if self.previous_price is None:
            self.previous_price = price
            return {"action": "HOLD", "quantity": 0}

        if price > self.previous_price * 1.02:
            signal = {"action": "BUY", "quantity": 1}
        elif price < self.previous_price * 0.98:
            signal = {"action": "SELL", "quantity": 1}
        else:
            signal = {"action": "HOLD", "quantity": 0}

        self.previous_price = price
        return signal

class StrategyFactory:
    _strategies = {
        'simple': SimpleStrategy,
        'momentum': MomentumStrategy,
        'always_buy': AlwaysBuyStrategy
    }

    @classmethod
    def get_strategy(cls, strategy_key: str) -> BaseStrategy:
        strategy_class = cls._strategies.get(strategy_key, SimpleStrategy)
        return strategy_class()