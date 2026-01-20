from django.db import models
from django.utils import timezone
from climate.models import ClimatePrediction


class Hive(models.Model):
    hive_id = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=200)
    installation_date = models.DateField(default=timezone.now)
    bee_species = models.CharField(max_length=100)
    queen_age_months = models.IntegerField()
    colony_size_estimate = models.IntegerField(help_text="Estimated number of bees")
    
    def __str__(self):
        return self.hive_id


class HiveActivity(models.Model):
    hive = models.ForeignKey(Hive, on_delete=models.CASCADE)
    recorded_at = models.DateTimeField(default=timezone.now)
    weight_kg = models.FloatField(help_text="Hive weight in kg")
    foraging_activity_level = models.IntegerField(choices=[(i, i) for i in range(1, 11)], help_text="1=low, 10=high")
    aggressiveness_score = models.IntegerField(choices=[(i, i) for i in range(1, 11)], help_text="1=calm, 10=aggressive")
    brood_presence = models.BooleanField(default=False)
    internal_temperature = models.FloatField(null=True, blank=True, help_text="Internal hive temperature in Celsius")
    ambient_temperature = models.FloatField(null=True, blank=True, help_text="Ambient temperature in Celsius")
    climate_prediction = models.ForeignKey(ClimatePrediction, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        ordering = ['-recorded_at']
    
    def __str__(self):
        return f"{self.hive.hive_id} - {self.recorded_at}"


class ColonyHealthPrediction(models.Model):
    hive = models.ForeignKey(Hive, on_delete=models.CASCADE)
    prediction_date = models.DateTimeField(default=timezone.now)
    honey_yield_estimation = models.FloatField(help_text="Estimated honey yield in kg")
    absconding_risk_score = models.FloatField(help_text="Risk of absconding (0-1)")
    swarming_probability = models.FloatField(help_text="Probability of swarming (0-1)")
    colony_stress_index = models.FloatField(help_text="Colony stress index (0-1)")
    health_status = models.CharField(max_length=50, choices=[
        ('healthy', 'Healthy'),
        ('moderate', 'Moderate Concern'),
        ('critical', 'Critical')
    ], default='healthy')
    
    def __str__(self):
        return f"Health prediction for {self.hive.hive_id}"
