from django.db import models

class BacktestRun(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата на теста")
    strategy_name = models.CharField(max_length=100, verbose_name="Стратегия")
    ticker = models.CharField(max_length=20, verbose_name="Актив")
    initial_capital = models.FloatField(verbose_name="Начален капитал")
    final_value = models.FloatField(verbose_name="Краен капитал")
    roi_percentage = models.FloatField(verbose_name="Възвръщаемост (ROI %)")
    max_drawdown = models.FloatField(verbose_name="Максимален спад (%)")

    def __str__(self):
        return f"Тест: {self.ticker} | Стратегия: {self.strategy_name} | ROI: {self.roi_percentage:.2f}%"


class Trade(models.Model):
    ACTION_CHOICES = [
        ('BUY', 'Покупка'),
        ('SELL', 'Продажба'),
    ]
    run = models.ForeignKey(BacktestRun, on_delete=models.CASCADE, related_name='trades')
    action = models.CharField(max_length=4, choices=ACTION_CHOICES, verbose_name="Действие")
    price = models.FloatField(verbose_name="Цена")
    quantity = models.IntegerField(verbose_name="Количество")
    date = models.CharField(max_length=20, verbose_name="Дата")
    def __str__(self):
        return f"{self.action} {self.quantity} бр. на цена {self.price} ({self.date})"
