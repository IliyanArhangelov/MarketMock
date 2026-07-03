import json
from datetime import datetime
from src.portfolio import Portfolio

class PerformanceReporter:
    """Генерирай и запазвай финансов отчет от симулацията."""

    def __init__(self, portfolio: Portfolio, daily_valuations: list):
        self.portfolio = portfolio
        self.daily_valuations = daily_valuations

    def calculate_roi(self) -> float:
        """Изчисли възвръщаемостта (ROI) в проценти."""
        if not self.daily_valuations:
            return 0.0
        
        initial_value = self.daily_valuations[0]["value"]
        final_value = self.daily_valuations[-1]["value"]
        
        roi = ((final_value - initial_value) / initial_value) * 100
        return roi

    def calculate_max_drawdown(self) -> float:
        """Изчисли максималния спад (Max Drawdown) в проценти."""
        max_drawdown = 0.0
        peak = -1.0

        for entry in self.daily_valuations:
            value = entry["value"]
            if value > peak:
                peak = value
            
            drawdown = ((peak - value) / peak) * 100
            if drawdown > max_drawdown:
                max_drawdown = drawdown
                
        return max_drawdown

    def generate_report(self) -> None:
        """Генерирай финален отчет, принтирай го и го запази в JSON файл."""
        roi = self.calculate_roi()
        max_dd = self.calculate_max_drawdown()
        
        final_value = self.daily_valuations[-1]["value"] if self.daily_valuations else self.portfolio.cash
        
        report_data = {
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_trades": len(self.portfolio.history),
            "final_value": round(final_value, 2),
            "roi_percentage": round(roi, 2),
            "max_drawdown_percentage": round(max_dd, 2)
        }
        
        print("\n" + "=" * 40)
        print("ФИНАНСОВ ОТЧЕТ".center(40))
        print("=" * 40)
        print(f"Краен капитал: {report_data['final_value']} USD")
        print(f"ROI (Възвръщаемост): {report_data['roi_percentage']}%")
        print(f"Максимален спад: {report_data['max_drawdown_percentage']}%")
        print(f"Общо сделки: {report_data['total_trades']}")
        print("=" * 40)
        
        with open("report.json", mode="w", encoding="utf-8") as file:
            json.dump(report_data, file, indent=4, ensure_ascii=False)
            
        print("\nОтчетът е запазен успешно в 'report.json'.")