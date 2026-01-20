from django.contrib import admin
from .models import ProductionPrediction, MarketData, PricePrediction, Recommendation

admin.site.register(ProductionPrediction)
admin.site.register(MarketData)
admin.site.register(PricePrediction)
admin.site.register(Recommendation)
