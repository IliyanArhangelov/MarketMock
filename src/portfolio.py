from src.exceptions import InsufficientFundsError
from src.logger import logger

class Portfolio:
    def __init__(self, initial_capital: float, fee_percent: float = 0.001):
        self.cash = initial_capital
        self.fee_percent = fee_percent
        self.positions = {} 
        self.history = []   

    def __len__(self):
        return len(self.history)

    def __getitem__(self, ticker: str):
        return self.positions.get(ticker, 0)

    def __contains__(self, ticker: str):
        return ticker in self.positions and self.positions[ticker] > 0

    def __iter__(self):
        return iter(self.positions.items())

    def buy(self, ticker: str, price: float, quantity: int, date: str):
        cost = price * quantity
        fee = cost * self.fee_percent
        total_cost = cost + fee

        if self.cash < total_cost:
            raise InsufficientFundsError(total_cost, self.cash)

        self.cash -= total_cost
        self.positions[ticker] = self[ticker] + quantity
        
        self.history.append({
            "action": "BUY",
            "ticker": ticker,
            "price": price,
            "quantity": quantity,
            "date": date
        })
        
        logger.info(f"Купени {quantity} бр. {ticker} на цена {price:.2f}. Такса: {fee:.2f}")

    def sell(self, ticker: str, price: float, quantity: int, date: str):
        current_qty = self[ticker]
        
        if current_qty < quantity:
            logger.warning(f"Опит за продажба на {quantity} {ticker}, но имаме само {current_qty}.")
            return

        revenue = price * quantity
        fee = revenue * self.fee_percent
        total_revenue = revenue - fee

        self.cash += total_revenue
        self.positions[ticker] -= quantity

        if self.positions[ticker] == 0:
            del self.positions[ticker]

        self.history.append({
            "action": "SELL",
            "ticker": ticker,
            "price": price,
            "quantity": quantity,
            "date": date
        })
        
        logger.info(f"Продадени {quantity} бр. {ticker} на цена {price:.2f}. Такса: {fee:.2f}")

    def get_total_value(self, current_prices: dict) -> float:
        value = self.cash
        for ticker, qty in self:
            if ticker in current_prices:
                value += qty * current_prices[ticker]
        return value

    def __str__(self):
        return f"Портфейл(Кеш: {self.cash:.2f}, Активи: {self.positions})"