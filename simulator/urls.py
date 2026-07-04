from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('result/<int:run_id>/', views.result_view, name='simulation_result'),
]