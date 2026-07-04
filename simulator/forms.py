from django import forms

class SimulationForm(forms.Form):
    initial_capital = forms.FloatField(
        label='Първоначален капитал (USD)',
        min_value=1.0,
        initial=1000.0,
        widget=forms.NumberInput(attrs={'class': 'form-control'}) 
    )

    csv_file = forms.FileField(
        label='Качи CSV файл с исторически данни',
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.csv'}) # accept ограничава само до .csv
    )