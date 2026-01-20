from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from .models import ProductionPrediction, MarketData, PricePrediction, Recommendation
from hives.models import Hive, ColonyHealthPrediction
from climate.models import ClimatePrediction
import json


def production_predictions(request):
    """API endpoint to get production predictions"""
    if request.method == 'GET':
        hive_id = request.GET.get('hive_id', '')
        start_date = request.GET.get('start_date', '')
        end_date = request.GET.get('end_date', '')
        
        queryset = ProductionPrediction.objects.all()
        
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
                'optimal_harvest_window_start': item.optimal_harvest_window_start,
                'optimal_harvest_window_end': item.optimal_harvest_window_end,
                'expected_production_volume': item.expected_production_volume,
                'feeding_necessity_alert': item.feeding_necessity_alert,
                'nectar_flow_probability': item.nectar_flow_probability,
            })
        
        return JsonResponse({'production_predictions': data})


def market_data_list(request):
    """API endpoint to get market data"""
    if request.method == 'GET':
        region = request.GET.get('region', '')
        product_type = request.GET.get('product_type', 'Honey')
        start_date = request.GET.get('start_date', '')
        end_date = request.GET.get('end_date', '')
        
        queryset = MarketData.objects.all()
        
        if region:
            queryset = queryset.filter(region__icontains=region)
        if product_type:
            queryset = queryset.filter(product_type__icontains=product_type)
        if start_date:
            queryset = queryset.filter(date_recorded__gte=start_date)
        if end_date:
            queryset = queryset.filter(date_recorded__lte=end_date)
        
        data = []
        for item in queryset:
            data.append({
                'id': item.id,
                'product_type': item.product_type,
                'region': item.region,
                'date_recorded': item.date_recorded,
                'price_per_kg': item.price_per_kg,
                'seasonal_demand_factor': item.seasonal_demand_factor,
                'regional_supply_indicator': item.regional_supply_indicator,
            })
        
        return JsonResponse({'market_data': data})


def price_predictions(request):
    """API endpoint to get price predictions"""
    if request.method == 'GET':
        region = request.GET.get('region', '')
        product_type = request.GET.get('product_type', 'Honey')
        start_date = request.GET.get('start_date', '')
        end_date = request.GET.get('end_date', '')
        
        queryset = PricePrediction.objects.all()
        
        if region:
            queryset = queryset.filter(region__icontains=region)
        if product_type:
            queryset = queryset.filter(product_type__icontains=product_type)
        if start_date:
            queryset = queryset.filter(prediction_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(prediction_date__lte=end_date)
        
        data = []
        for item in queryset:
            data.append({
                'id': item.id,
                'product_type': item.product_type,
                'region': item.region,
                'prediction_date': item.prediction_date,
                'forecast_date': item.forecast_date,
                'predicted_price_per_kg': item.predicted_price_per_kg,
                'price_trend_forecast': item.price_trend_forecast,
                'hold_vs_sell_recommendation': item.hold_vs_sell_recommendation,
                'best_market_timing': item.best_market_timing,
            })
        
        return JsonResponse({'price_predictions': data})


def recommendations_list(request):
    """API endpoint to get recommendations"""
    if request.method == 'GET':
        hive_id = request.GET.get('hive_id', '')
        recommendation_type = request.GET.get('recommendation_type', '')
        start_date = request.GET.get('start_date', '')
        end_date = request.GET.get('end_date', '')
        priority = request.GET.get('priority', '')
        
        queryset = Recommendation.objects.all()
        
        if hive_id:
            queryset = queryset.filter(hive__hive_id=hive_id)
        if recommendation_type:
            queryset = queryset.filter(recommendation_type=recommendation_type)
        if start_date:
            queryset = queryset.filter(created_at__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__lte=end_date)
        if priority:
            queryset = queryset.filter(priority=priority)
        
        data = []
        for item in queryset:
            data.append({
                'id': item.id,
                'hive_id': item.hive.hive_id,
                'created_at': item.created_at,
                'recommendation_type': item.recommendation_type,
                'title': item.title,
                'description': item.description,
                'priority': item.priority,
                'is_action_required': item.is_action_required,
                'climate_prediction_id': item.climate_prediction.id if item.climate_prediction else None,
                'health_prediction_id': item.health_prediction.id if item.health_prediction else None,
                'production_prediction_id': item.production_prediction.id if item.production_prediction else None,
                'market_prediction_id': item.market_prediction.id if item.market_prediction else None,
            })
        
        return JsonResponse({'recommendations': data})


@csrf_exempt
def create_production_prediction(request):
    """API endpoint to create production prediction"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            hive = Hive.objects.get(hive_id=data['hive_id'])
            
            prod_pred = ProductionPrediction.objects.create(
                hive=hive,
                optimal_harvest_window_start=data['optimal_harvest_window_start'],
                optimal_harvest_window_end=data['optimal_harvest_window_end'],
                expected_production_volume=data['expected_production_volume'],
                feeding_necessity_alert=data['feeding_necessity_alert'],
                nectar_flow_probability=data['nectar_flow_probability'],
            )
            return JsonResponse({'success': True, 'id': prod_pred.id})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})


@csrf_exempt
def create_market_data(request):
    """API endpoint to create market data"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            market_data = MarketData.objects.create(
                product_type=data['product_type'],
                region=data['region'],
                price_per_kg=data['price_per_kg'],
                seasonal_demand_factor=data['seasonal_demand_factor'],
                regional_supply_indicator=data['regional_supply_indicator'],
            )
            return JsonResponse({'success': True, 'id': market_data.id})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})


@csrf_exempt
def create_price_prediction(request):
    """API endpoint to create price prediction"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            price_pred = PricePrediction.objects.create(
                product_type=data['product_type'],
                region=data['region'],
                forecast_date=data['forecast_date'],
                predicted_price_per_kg=data['predicted_price_per_kg'],
                price_trend_forecast=data['price_trend_forecast'],
                hold_vs_sell_recommendation=data['hold_vs_sell_recommendation'],
                best_market_timing=data['best_market_timing'],
            )
            return JsonResponse({'success': True, 'id': price_pred.id})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})


@csrf_exempt
def create_recommendation(request):
    """API endpoint to create recommendation"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            hive = Hive.objects.get(hive_id=data['hive_id'])
            
            # Get related predictions
            climate_pred = None
            health_pred = None
            prod_pred = None
            market_pred = None
            
            if 'climate_prediction_id' in data:
                climate_pred = ClimatePrediction.objects.get(id=data['climate_prediction_id'])
            if 'health_prediction_id' in data:
                health_pred = ColonyHealthPrediction.objects.get(id=data['health_prediction_id'])
            if 'production_prediction_id' in data:
                prod_pred = ProductionPrediction.objects.get(id=data['production_prediction_id'])
            if 'market_prediction_id' in data:
                market_pred = PricePrediction.objects.get(id=data['market_prediction_id'])
            
            recommendation = Recommendation.objects.create(
                hive=hive,
                recommendation_type=data['recommendation_type'],
                title=data['title'],
                description=data['description'],
                priority=data['priority'],
                is_action_required=data.get('is_action_required', True),
                climate_prediction=climate_pred,
                health_prediction=health_pred,
                production_prediction=prod_pred,
                market_prediction=market_pred,
            )
            return JsonResponse({'success': True, 'id': recommendation.id})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
