import csv
import requests
from datetime import datetime
from src.exceptions import InvalidDataError, MarketMockError
from src.logger import logger

def csv_data_generator(filepath: str):
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

def api_data_generator(symbol: str):
    url = "https://api.binance.com/api/v3/klines"
    params = {"symbol": symbol, "interval": "1d", "limit": 100}
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        for candle in data:
            date_str = datetime.fromtimestamp(candle[0] / 1000).strftime('%Y-%m-%d')
            close_price = candle[4]
            
            row = {"Date": date_str, "Close": close_price}
            yield row
            
    except requests.RequestException as e:
        logger.error(f"Грешка при връзка с API: {e}")
        raise MarketMockError(f"Неуспешно извличане на данни от Binance API: {e}")