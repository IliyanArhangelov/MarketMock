from typing import Generator, Dict
from src.portfolio import Portfolio
from src.strategies import BaseStrategy
from src.exceptions import InsufficientFundsError
from src.logger import logger

class MarketEngine:
    """Управлявай времевата линия и синхронизирай данните с портфейла."""

    def __init__(self, data_feed, portfolio, strategy, ticker: str):
        self.data_feed = data_feed
        self.portfolio = portfolio
        self.strategy = strategy
        self.ticker = ticker
        self.daily_valuations = []


    def run(self):
        """Стартирай симулацията, обхождайки данните ден по ден."""
        logger.info("--- СТАРТИРАНЕ НА СИМУЛАЦИЯТА ---")

        for daily_data in self.data_feed:
            date = daily_data.get("Date", "Unknown")
            
            try:
                price = float(daily_data["Close"])
            except ValueError:
                logger.warning(f"Пропуснат ден {date} поради невалидна цена.")
                continue

            signal = self.strategy.generate_signal(daily_data, self.portfolio.cash)

            action = signal.get("action")
            quantity = signal.get("quantity", 0)
            ticker = self.ticker
            if action == "BUY" and quantity > 0:
                try:
                    self.portfolio.buy(ticker, price, quantity, date)
                except InsufficientFundsError as e:
                    logger.warning(f"Отказана покупка на {date}: {e}")
                    
            elif action == "SELL" and quantity > 0:
                self.portfolio.sell(ticker, price, quantity, date)

            current_prices = {ticker: price}
            current_value = self.portfolio.get_total_value(current_prices)
            self.daily_valuations.append({
                "date": date,
                "value": current_value
            })

        logger.info("--- КРАЙ НА СИМУЛАЦИЯТА ---")