import unittest
from unittest.mock import Mock
from src.engine import MarketEngine
from src.portfolio import Portfolio

class TestMarketEngine(unittest.TestCase):

    def setUp(self):
        self.mock_data = [
            {"Date": "2024-01-01", "Close": "100.0"},
            {"Date": "2024-01-02", "Close": "150.0"}
        ]
        self.portfolio = Portfolio(1000.0)
        self.mock_strategy = Mock()

    def test_engine_run(self):
        self.mock_strategy.generate_signal.side_effect = [
            {"action": "BUY", "quantity": 1},
            {"action": "SELL", "quantity": 1}
        ]
        
        engine = MarketEngine(self.mock_data, self.portfolio, self.mock_strategy, "TEST")
        engine.run()

        self.assertEqual(self.mock_strategy.generate_signal.call_count, 2)
        self.assertEqual(len(engine.daily_valuations), 2)

if __name__ == "__main__":
    unittest.main()