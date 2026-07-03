import unittest
from src.portfolio import Portfolio
from src.exceptions import InsufficientFundsError

class TestPortfolio(unittest.TestCase):
    
    def setUp(self):
        self.portfolio = Portfolio(initial_capital=1000.0, fee_percent=0.01)

    def test_buy_success(self):
        self.portfolio.buy("AAPL", 100.0, 2, "2024-01-01")
        
        self.assertEqual(self.portfolio.cash, 798.0)
        self.assertEqual(self.portfolio.positions["AAPL"], 2)

    def test_buy_insufficient_funds(self):
        with self.assertRaises(InsufficientFundsError):
            self.portfolio.buy("AAPL", 1000.0, 2, "2024-01-01")

    def test_sell_success(self):
        self.portfolio.positions["AAPL"] = 2
        
        self.portfolio.sell("AAPL", 150.0, 1, "2024-01-02")
        
        self.assertEqual(self.portfolio.cash, 1148.5)
        self.assertEqual(self.portfolio.positions["AAPL"], 1)

if __name__ == "__main__":
    unittest.main()