from django.contrib import admin
from .models import BacktestRun, Trade

admin.site.register(BacktestRun)
admin.site.register(Trade)

