import sys
from src.data_loader import csv_data_generator
from src.portfolio import Portfolio
from src.strategies import SimpleStrategy
from src.engine import MarketEngine
from src.reporter import PerformanceReporter
from src.logger import logger

def main():
    print("=" * 50)
    print("      Добре дошли в MarketMock v1.0      ")
    print("=" * 50)

    while True:
        try:
            capital_input = input("\nВъведете първоначален виртуален капитал (USD): ")
            initial_capital = float(capital_input)
            if initial_capital <= 0:
                print("Капиталът трябва да е положително число!")
                continue
            break
        except ValueError:
            print("Моля, въведете валидно число.")

    print("\nИзберете източник на исторически данни:")
    print("[1] Локален CSV файл (data/sample.csv)")
    print("[2] Външно API (Binance) - Предстои да се добави")
    
    while True:
        data_source_choice = input("> ")
        if data_source_choice == "1":
            filepath = input("Въведете път до файла [натиснете Enter за 'data/sample.csv']: ")
            if not filepath:
                filepath = "data/sample.csv"
            data_gen = csv_data_generator(filepath)
            ticker_symbol = "CSV_ASSET"
            break
        elif data_source_choice == "2":
            print("API функционалността все още не е активна. Използваме CSV по подразбиране.")
            data_gen = csv_data_generator("data/sample.csv")
            ticker_symbol = "CSV_ASSET"
            break
        else:
            print("Невалиден избор. Моля, въведете 1 или 2.")

    print("\nИзберете търговска стратегия:")
    print("[1] Проста стратегия (Купува при спад, продава при ръст)")
    
    while True:
        strategy_choice = input("> ")
        if strategy_choice == "1":
            strategy = SimpleStrategy()
            break
        else:
            print("Невалиден избор. Моля, въведете 1.")

    print("\nКонфигурацията е успешна! Стартиране на симулацията...\n")
    
    portfolio = Portfolio(initial_capital=initial_capital)
    
    engine = MarketEngine(
        data_feed=data_gen,
        portfolio=portfolio,
        strategy=strategy,
        ticker=ticker_symbol
    )

    engine.run()

    reporter = PerformanceReporter(portfolio, engine.daily_valuations)
    reporter.generate_report()

if __name__ == "__main__":
    main()