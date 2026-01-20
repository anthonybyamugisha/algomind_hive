from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return render(request, 'index.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def climate_data(request):
    return render(request, 'climate_data.html')

def hive_management(request):
    return render(request, 'hive_management.html')

def ai_predictions(request):
    return render(request, 'ai_predictions.html')
