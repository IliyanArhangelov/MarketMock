from django import forms

class SimulationForm(forms.Form):
    STRATEGY_CHOICES = [
        ('simple', 'Simple Strategy (Buy < 100, Sell > 150)'),
        ('momentum', 'Momentum Strategy (Buy on +2% up, Sell on -2% down)'),
        ('always_buy', 'Aggressive (Always Buy if cash available)'),
    ]

    initial_capital = forms.FloatField(
        label='Първоначален капитал (USD)',
        min_value=1.0,
        initial=1000.0,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    
    strategy = forms.ChoiceField(
        choices=STRATEGY_CHOICES,
        label='Търговска стратегия',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    csv_file = forms.FileField(
        label='Качи CSV файл с исторически данни',
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.csv'})
    )