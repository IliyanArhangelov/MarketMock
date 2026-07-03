# src/strategies.py
from src.logger import logger

def log_signal(func):
    """Логни генерирания сигнал от стратегията."""
    def decorated(*args, **kwargs):
        signal = func(*args, **kwargs)
        if signal["action"] != "HOLD":
            logger.info(f"Стратегията реши: {signal['action']} {signal['quantity']} бр.")
            
        return signal
    return decorated


class BaseStrategy:
    """Служи като базов клас за всички търговски стратегии."""

    def generate_signal(self, current_data: dict, current_cash: float) -> dict:
        """Генерирай сигнал за търговия. Трябва да се презапише от класа-наследник."""
        raise NotImplementedError("Този метод трябва да се презапише.")


class SimpleStrategy(BaseStrategy):
    """Купувай, ако цената е под 100, продавай, ако е над 150."""

    @log_signal
    def generate_signal(self, current_data: dict, current_cash: float) -> dict:
        """Върни конкретен сигнал на база текущата цена."""
        price = float(current_data["Close"])
        
        if price < 100.0:
            return {"action": "BUY", "quantity": 1}
        elif price > 150.0:
            return {"action": "SELL", "quantity": 1}
        else:
            return {"action": "HOLD", "quantity": 0}