from django.shortcuts import render, redirect, get_object_or_404
from .forms import SimulationForm
from .runner import execute_simulation
from .models import BacktestRun

def home_view(request):
    if request.method == 'POST':
        form = SimulationForm(request.POST, request.FILES) 
        if form.is_valid():
            capital = form.cleaned_data['initial_capital']
            strategy_key = form.cleaned_data['strategy']
            uploaded_file = form.cleaned_data['csv_file']
            
            run_id = execute_simulation(capital, strategy_key, uploaded_file)
            
            return redirect('simulation_result', run_id=run_id)
    else:
        form = SimulationForm()
        
    return render(request, 'simulator/home.html', {'form': form})

def result_view(request, run_id):
    run_record = get_object_or_404(BacktestRun, id=run_id)
    trades = run_record.trades.all()
    
    return render(request, 'simulator/result.html', {
        'run': run_record,
        'trades': trades
    })