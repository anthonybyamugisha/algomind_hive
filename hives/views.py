from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from .models import Hive, HiveActivity, ColonyHealthPrediction
from climate.models import ClimatePrediction
import json


def hive_list(request):
    """API endpoint to get hives"""
    if request.method == 'GET':
        location = request.GET.get('location', '')
        species = request.GET.get('species', '')
        
        queryset = Hive.objects.all()
        
        if location:
            queryset = queryset.filter(location__icontains=location)
        if species:
            queryset = queryset.filter(bee_species__icontains=species)
        
        data = []
        for item in queryset:
            data.append({
                'id': item.id,
                'hive_id': item.hive_id,
                'location': item.location,
                'installation_date': item.installation_date,
                'bee_species': item.bee_species,
                'queen_age_months': item.queen_age_months,
                'colony_size_estimate': item.colony_size_estimate,
            })
        
        return JsonResponse({'hives': data})


def hive_activity_list(request):
    """API endpoint to get hive activity"""
    if request.method == 'GET':
        hive_id = request.GET.get('hive_id', '')
        start_date = request.GET.get('start_date', '')
        end_date = request.GET.get('end_date', '')
        
        queryset = HiveActivity.objects.all()
        
        if hive_id:
            queryset = queryset.filter(hive__hive_id=hive_id)
        if start_date:
            queryset = queryset.filter(recorded_at__gte=start_date)
        if end_date:
            queryset = queryset.filter(recorded_at__lte=end_date)
        
        data = []
        for item in queryset:
            data.append({
                'id': item.id,
                'hive_id': item.hive.hive_id,
                'recorded_at': item.recorded_at,
                'weight_kg': item.weight_kg,
                'foraging_activity_level': item.foraging_activity_level,
                'aggressiveness_score': item.aggressiveness_score,
                'brood_presence': item.brood_presence,
                'internal_temperature': item.internal_temperature,
                'ambient_temperature': item.ambient_temperature,
                'climate_prediction_id': item.climate_prediction.id if item.climate_prediction else None,
            })
        
        return JsonResponse({'hive_activities': data})


def colony_health_predictions(request):
    """API endpoint to get colony health predictions"""
    if request.method == 'GET':
        hive_id = request.GET.get('hive_id', '')
        start_date = request.GET.get('start_date', '')
        end_date = request.GET.get('end_date', '')
        
        queryset = ColonyHealthPrediction.objects.all()
        
        if hive_id:
            queryset = queryset.filter(hive__hive_id=hive_id)
        if start_date:
            queryset = queryset.filter(prediction_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(prediction_date__lte=end_date)
        
        data = []
        for item in queryset:
            data.append({
                'id': item.id,
                'hive_id': item.hive.hive_id,
                'prediction_date': item.prediction_date,
                'honey_yield_estimation': item.honey_yield_estimation,
                'absconding_risk_score': item.absconding_risk_score,
                'swarming_probability': item.swarming_probability,
                'colony_stress_index': item.colony_stress_index,
                'health_status': item.health_status,
            })
        
        return JsonResponse({'colony_health_predictions': data})


@csrf_exempt
def create_hive(request):
    """API endpoint to create a hive"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            hive = Hive.objects.create(
                hive_id=data['hive_id'],
                location=data['location'],
                bee_species=data['bee_species'],
                queen_age_months=data['queen_age_months'],
                colony_size_estimate=data['colony_size_estimate'],
            )
            return JsonResponse({'success': True, 'id': hive.id})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})


@csrf_exempt
def create_hive_activity(request):
    """API endpoint to create hive activity"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Get the hive instance
            hive = Hive.objects.get(hive_id=data['hive_id'])
            
            # Optionally get climate prediction
            climate_prediction = None
            if 'climate_prediction_id' in data:
                climate_prediction = ClimatePrediction.objects.get(id=data['climate_prediction_id'])
            
            activity = HiveActivity.objects.create(
                hive=hive,
                weight_kg=data['weight_kg'],
                foraging_activity_level=data['foraging_activity_level'],
                aggressiveness_score=data['aggressiveness_score'],
                brood_presence=data['brood_presence'],
                internal_temperature=data.get('internal_temperature'),
                ambient_temperature=data.get('ambient_temperature'),
                climate_prediction=climate_prediction,
            )
            return JsonResponse({'success': True, 'id': activity.id})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
