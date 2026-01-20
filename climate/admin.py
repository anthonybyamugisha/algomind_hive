from django.contrib import admin
from .models import ClimateData, ClimatePrediction

admin.site.register(ClimateData)
admin.site.register(ClimatePrediction)
