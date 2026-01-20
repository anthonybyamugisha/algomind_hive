from django.db import models
from django.utils import timezone
from hives.models import Hive, ColonyHealthPrediction
from climate.models import ClimatePrediction


class ProductionPrediction(models.Model):
    hive = models.ForeignKey(Hive, on_delete=models.CASCADE)
    prediction_date = models.DateTimeField(default=timezone.now)
    optimal_harvest_window_start = models.DateField()
    optimal_harvest_window_end = models.DateField()
    expected_production_volume = models.FloatField(help_text="Expected honey production in kg")
    feeding_necessity_alert = models.BooleanField(default=False)
    nectar_flow_probability = models.FloatField(help_text="Probability of good nectar flow (0-1)")
    
    def __str__(self):
        return f"Production prediction for {self.hive.hive_id}"


class MarketData(models.Model):
    product_type = models.CharField(max_length=100, default="Honey")
    region = models.CharField(max_length=200)
    date_recorded = models.DateField(default=timezone.now)
    price_per_kg = models.FloatField(help_text="Price per kg in local currency")
    seasonal_demand_factor = models.FloatField(help_text="Demand factor relative to annual average")
    regional_supply_indicator = models.FloatField(help_text="Supply indicator (0-1)")
    
    def __str__(self):
        return f"{self.product_type} price in {self.region} - {self.date_recorded}"


class PricePrediction(models.Model):
    product_type = models.CharField(max_length=100, default="Honey")
    region = models.CharField(max_length=200)
    prediction_date = models.DateTimeField(default=timezone.now)
    forecast_date = models.DateField()
    predicted_price_per_kg = models.FloatField(help_text="Predicted price per kg in local currency")
    price_trend_forecast = models.FloatField(help_text="Price trend indicator (-1 to 1)")
    hold_vs_sell_recommendation = models.CharField(max_length=20, choices=[
        ('hold', 'Hold'),
        ('sell', 'Sell')
    ])
    best_market_timing = models.FloatField(help_text="Optimal timing score (0-1)")
    
    def __str__(self):
        return f"Price prediction for {self.product_type} in {self.region}"


class Recommendation(models.Model):
    hive = models.ForeignKey(Hive, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    recommendation_type = models.CharField(max_length=100, choices=[
        ('absconding_risk', 'Absconding Risk Mitigation'),
        ('nectar_flow', 'Nectar Flow Preparation'),
        ('harvest_timing', 'Harvest Timing'),
        ('feeding_schedule', 'Feeding Schedule'),
        ('market_timing', 'Market Timing')
    ])
    title = models.CharField(max_length=200)
    description = models.TextField()
    priority = models.IntegerField(choices=[(i, i) for i in range(1, 6)], help_text="1=highest priority, 5=lowest priority")
    is_action_required = models.BooleanField(default=True)
    climate_prediction = models.ForeignKey(ClimatePrediction, on_delete=models.SET_NULL, null=True, blank=True)
    health_prediction = models.ForeignKey(ColonyHealthPrediction, on_delete=models.SET_NULL, null=True, blank=True)
    production_prediction = models.ForeignKey('ProductionPrediction', on_delete=models.SET_NULL, null=True, blank=True)
    market_prediction = models.ForeignKey('PricePrediction', on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} for {self.hive.hive_id}"
