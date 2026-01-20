from django.urls import path
from . import views

urlpatterns = [
    path('production-predictions/', views.production_predictions, name='production-predictions-list'),
    path('market-data/', views.market_data_list, name='market-data-list'),
    path('price-predictions/', views.price_predictions, name='price-predictions-list'),
    path('recommendations/', views.recommendations_list, name='recommendations-list'),
    path('create-production-prediction/', views.create_production_prediction, name='create-production-prediction'),
    path('create-market-data/', views.create_market_data, name='create-market-data'),
    path('create-price-prediction/', views.create_price_prediction, name='create-price-prediction'),
    path('create-recommendation/', views.create_recommendation, name='create-recommendation'),
]