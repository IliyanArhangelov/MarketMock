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
    """Купувай при спад, продавай при ръст."""
    
    BUY_THRESHOLD = 100.0
    SELL_THRESHOLD = 150.0

    @log_signal
    def generate_signal(self, current_data: dict, current_cash: float) -> dict:
        """Върни конкретен сигнал на база текущата цена."""
        price = float(current_data["Close"])
        
        if price < self.BUY_THRESHOLD:
            return {"action": "BUY", "quantity": 1}
        elif price > self.SELL_THRESHOLD:
            return {"action": "SELL", "quantity": 1}
        else:
            return {"action": "HOLD", "quantity": 0}