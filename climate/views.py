from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from .models import ClimateData, ClimatePrediction
import json


def climate_data_list(request):
    """API endpoint to get climate data"""
    if request.method == 'GET':
        location = request.GET.get('location', '')
        start_date = request.GET.get('start_date', '')
        end_date = request.GET.get('end_date', '')
        
        queryset = ClimateData.objects.all()
        
        if location:
            queryset = queryset.filter(location__icontains=location)
        if start_date:
            queryset = queryset.filter(date_recorded__gte=start_date)
        if end_date:
            queryset = queryset.filter(date_recorded__lte=end_date)
        
        data = []
        for item in queryset:
            data.append({
                'id': item.id,
                'location': item.location,
                'latitude': item.latitude,
                'longitude': item.longitude,
                'date_recorded': item.date_recorded,
                'temperature_min': item.temperature_min,
                'temperature_max': item.temperature_max,
                'rainfall': item.rainfall,
                'humidity_avg': item.humidity_avg,
                'seasonal_trend': item.seasonal_trend,
            })
        
        return JsonResponse({'climate_data': data})


def climate_prediction_list(request):
    """API endpoint to get climate predictions"""
    if request.method == 'GET':
        location = request.GET.get('location', '')
        start_date = request.GET.get('start_date', '')
        end_date = request.GET.get('end_date', '')
        
        queryset = ClimatePrediction.objects.all()
        
        if location:
            queryset = queryset.filter(location__icontains=location)
        if start_date:
            queryset = queryset.filter(forecast_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(forecast_date__lte=end_date)
        
        data = []
        for item in queryset:
            data.append({
                'id': item.id,
                'location': item.location,
                'prediction_date': item.prediction_date,
                'forecast_date': item.forecast_date,
                'predicted_temperature_min': item.predicted_temperature_min,
                'predicted_temperature_max': item.predicted_temperature_max,
                'predicted_rainfall': item.predicted_rainfall,
                'predicted_humidity': item.predicted_humidity,
                'nectar_flow_probability': item.nectar_flow_probability,
                'heat_stress_index': item.heat_stress_index,
                'moisture_stress_index': item.moisture_stress_index,
            })
        
        return JsonResponse({'climate_predictions': data})


@csrf_exempt
def create_climate_data(request):
    """API endpoint to create climate data"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            climate_data = ClimateData.objects.create(
                location=data['location'],
                latitude=data['latitude'],
                longitude=data['longitude'],
                temperature_min=data['temperature_min'],
                temperature_max=data['temperature_max'],
                rainfall=data['rainfall'],
                humidity_avg=data['humidity_avg'],
                seasonal_trend=data['seasonal_trend'],
            )
            return JsonResponse({'success': True, 'id': climate_data.id})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})


@csrf_exempt
def create_climate_prediction(request):
    """API endpoint to create climate prediction"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            climate_pred = ClimatePrediction.objects.create(
                location=data['location'],
                forecast_date=data['forecast_date'],
                predicted_temperature_min=data['predicted_temperature_min'],
                predicted_temperature_max=data['predicted_temperature_max'],
                predicted_rainfall=data['predicted_rainfall'],
                predicted_humidity=data['predicted_humidity'],
                nectar_flow_probability=data['nectar_flow_probability'],
                heat_stress_index=data['heat_stress_index'],
                moisture_stress_index=data['moisture_stress_index'],
            )
            return JsonResponse({'success': True, 'id': climate_pred.id})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
