from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm


def home(request):
    return render(request, 'index.html')

def dashboard(request):
    # Check which specific dashboard page is requested
    page = request.path.split('/')[-1]
    if page == 'main' or 'dashboard-main' in request.path:
        return render(request, 'dashboard_main.html')
    return render(request, 'dashboard.html')

def climate_data(request):
    # Check which specific climate page is requested
    page = request.path.split('/')[-1]
    if page == 'environment' or 'climate-environment' in request.path:
        return render(request, 'climate_environment.html')
    return render(request, 'climate_data.html')

def hive_management(request):
    # Check which specific hive page is requested
    page = request.path.split('/')[-1]
    if page == 'observation' or 'hive-observation' in request.path:
        return render(request, 'hive_observation.html')
    return render(request, 'hive_management.html')

def ai_predictions(request):
    # Check which specific AI page is requested
    page = request.path.split('/')[-1]
    if page == 'recommendations' or 'predictions-recommendations' in request.path:
        return render(request, 'predictions_recommendations.html')
    elif page == 'price' or 'market-price' in request.path:
        return render(request, 'market_price.html')
    return render(request, 'ai_predictions.html')

def login_view(request):
    return render(request, 'registration/login.html')

def register_view(request):
    return render(request, 'registration/register.html')
