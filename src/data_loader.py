import csv
from typing import Dict
from src.exceptions import InvalidDataError, MarketMockError
from src.logger import logger

def csv_data_generator(filepath: str):
    """Чети CSV файла ред по ред."""
    try:
        with open(filepath, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                if "Close" not in row or not row["Close"]:
                    logger.error("Намерен е ред без цена.")
                    raise InvalidDataError(row, "Липсва колона 'Close' или е празна")
                
                try:
                    float(row["Close"])
                except ValueError:
                    logger.error("Цената не може да се обърне във float.")
                    raise InvalidDataError(row, "Цената не е валидно число")
                
                yield row
                
    except FileNotFoundError:
        logger.error(f"Файлът {filepath} не беше намерен.")
        raise MarketMockError(f"Файлът {filepath} не съществува. Провери пътя!")