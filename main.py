from src.data_loader import csv_data_generator
from src.portfolio import Portfolio
from src.strategies import SimpleStrategy
from src.engine import MarketEngine
from src.reporter import PerformanceReporter
from src.logger import logger

def main():
    csv_file_path = "data/sample.csv"
    ticker_symbol = "TEST_ASSET"

    logger.info("=== Инициализация на системата ===")

    data_gen = csv_data_generator(csv_file_path)
    my_portfolio = Portfolio(initial_capital=1000.0)
    my_strategy = SimpleStrategy()

    engine = MarketEngine(
        data_feed=data_gen, 
        portfolio=my_portfolio, 
        strategy=my_strategy, 
        ticker=ticker_symbol
    )

    engine.run()

    reporter = PerformanceReporter(my_portfolio, engine.daily_valuations)
    reporter.generate_report()

if __name__ == "__main__":
    main()