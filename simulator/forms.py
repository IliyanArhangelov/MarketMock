from django import forms

class SimulationForm(forms.Form):
    STRATEGY_CHOICES = [
        ('simple', 'Simple Strategy (Buy < 100, Sell > 150)'),
        ('momentum', 'Momentum Strategy (Buy on +2% up, Sell on -2% down)'),
        ('always_buy', 'Aggressive (Always Buy if cash available)'),
    ]

    SOURCE_CHOICES = [
        ('csv', 'Локален CSV файл'),
        ('api', 'Външно API (Binance)'),
    ]

    initial_capital = forms.FloatField(
        label='Първоначален капитал (USD)',
        min_value=1.0,
        initial=100000.0,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    
    strategy = forms.ChoiceField(
        choices=STRATEGY_CHOICES,
        label='Търговска стратегия',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    data_source = forms.ChoiceField(
        choices=SOURCE_CHOICES,
        label='Източник на данни',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    csv_file = forms.FileField(
        label='Качи CSV файл (ако си избрал CSV)',
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.csv'})
    )

    ticker = forms.CharField(
        label='Символ (ако си избрал API, напр. BTCUSDT)',
        required=False,
        initial='BTCUSDT',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    def clean(self):
        cleaned_data = super().clean()
        data_source = cleaned_data.get('data_source')
        csv_file = cleaned_data.get('csv_file')
        ticker = cleaned_data.get('ticker')

        if data_source == 'csv' and not csv_file:
            self.add_error('csv_file', 'Моля, качете CSV файл.')
        elif data_source == 'api' and not ticker:
            self.add_error('ticker', 'Моля, въведете символ за API-то.')

        return cleaned_data