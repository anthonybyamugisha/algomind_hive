from django.db import models
from django.utils import timezone


class ClimateData(models.Model):
    location = models.CharField(max_length=200)
    latitude = models.FloatField()
    longitude = models.FloatField()
    date_recorded = models.DateField(default=timezone.now)
    temperature_min = models.FloatField(help_text="Minimum temperature in Celsius")
    temperature_max = models.FloatField(help_text="Maximum temperature in Celsius")
    rainfall = models.FloatField(help_text="Rainfall in mm")
    humidity_avg = models.FloatField(help_text="Average humidity percentage")
    seasonal_trend = models.CharField(max_length=100, choices=[
        ('spring', 'Spring'),
        ('summer', 'Summer'),
        ('autumn', 'Autumn'),
        ('winter', 'Winter')
    ])
    
    def __str__(self):
        return f"{self.location} - {self.date_recorded}"


class ClimatePrediction(models.Model):
    location = models.CharField(max_length=200)
    prediction_date = models.DateTimeField(default=timezone.now)
    forecast_date = models.DateField()
    predicted_temperature_min = models.FloatField()
    predicted_temperature_max = models.FloatField()
    predicted_rainfall = models.FloatField()
    predicted_humidity = models.FloatField()
    nectar_flow_probability = models.FloatField(help_text="Probability of good nectar flow (0-1)")
    heat_stress_index = models.FloatField(help_text="Heat stress indicator (0-1)")
    moisture_stress_index = models.FloatField(help_text="Moisture stress indicator (0-1)")
    
    def __str__(self):
        return f"Climate prediction for {self.location} on {self.forecast_date}"
