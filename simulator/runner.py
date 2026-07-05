import os
import tempfile
from simulator.models import BacktestRun, Trade
from src.portfolio import Portfolio
from src.strategies import StrategyFactory
from src.data_loader import csv_data_generator, api_data_generator
from src.engine import MarketEngine

def execute_simulation(initial_capital: float, strategy_key: str, data_source: str, uploaded_file=None, ticker: str=None) -> int:
    temp_file_path = None
    
    if data_source == 'csv':
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp_file:
            for chunk in uploaded_file.chunks():
                tmp_file.write(chunk)
            temp_file_path = tmp_file.name 
        data_gen = csv_data_generator(temp_file_path)
        run_ticker = uploaded_file.name
    else:
        data_gen = api_data_generator(ticker)
        run_ticker = ticker

    try:
        portfolio = Portfolio(initial_capital=initial_capital)
        strategy = StrategyFactory.get_strategy(strategy_key)
        
        engine = MarketEngine(
            data_feed=data_gen,
            portfolio=portfolio,
            strategy=strategy,
            ticker=run_ticker
        )
        
        engine.run()
        
        roi = 0.0
        max_dd = 0.0
        final_value = portfolio.cash
        
        if engine.daily_valuations:
            initial_value = engine.daily_valuations[0]["value"]
            final_value = engine.daily_valuations[-1]["value"]
            roi = ((final_value - initial_value) / initial_value) * 100
            
            peak = -1.0
            for entry in engine.daily_valuations:
                val = entry["value"]
                if val > peak: 
                    peak = val
                dd = ((peak - val) / peak) * 100
                if dd > max_dd: 
                    max_dd = dd

        run_record = BacktestRun.objects.create(
            strategy_name=strategy.__class__.__name__,
            ticker=run_ticker,
            initial_capital=initial_capital,
            final_value=final_value,
            roi_percentage=roi,
            max_drawdown=max_dd
        )
        
        trades_to_create = [
            Trade(
                run=run_record,
                action=t["action"],
                price=t["price"],
                quantity=t["quantity"],
                date=t["date"]
            ) for t in portfolio.history
        ]
        Trade.objects.bulk_create(trades_to_create)
        
        return run_record.id

    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)